"""Stripe payment utilities for ride donations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Optional

import stripe
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.donation import Donation
from app.models.ride import Ride
from app.models.ride_request import RideRequest
from app.models.user import User


class StripeNotConfiguredError(RuntimeError):
    """Raised when Stripe settings are not configured."""


@dataclass(frozen=True)
class DonationIntentResult:
    payment_intent_id: str
    client_secret: str
    amount_cents: int


class PaymentService:
    """Encapsulates Stripe operations for donations."""

    SUGGESTED_DONATION_AMOUNTS_CENTS = [500, 1000, 1500, 2000]  # $5, $10, $15, $20

    def __init__(self) -> None:
        if not settings.STRIPE_SECRET_KEY:
            raise StripeNotConfiguredError("Stripe is not configured (STRIPE_SECRET_KEY missing).")
        stripe.api_key = settings.STRIPE_SECRET_KEY

    @staticmethod
    def calculate_stripe_fee_cents(amount_cents: int) -> int:
        """Estimate Stripe's fee: 2.9% + $0.30 (USD)."""
        if amount_cents <= 0:
            return 0
        pct_fee = (Decimal(amount_cents) * Decimal("0.029")).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        )
        return int(pct_fee) + 30

    @classmethod
    def suggest_donation_amount_cents(
        cls,
        distance_miles: float,
        *,
        base_cents: int = 500,
        per_mile_cents: int = 50,
        min_cents: int = 100,
        max_cents: int = 100_000,
    ) -> int:
        """Suggest a donation based on distance (simple heuristic)."""
        if distance_miles < 0:
            distance_miles = 0
        suggested = int(base_cents + (distance_miles * per_mile_cents))
        return max(min_cents, min(max_cents, suggested))

    def get_or_create_stripe_customer_id(self, db: Session, *, user: User) -> str:
        """Get/create a Stripe Customer and persist the ID on the user."""
        if user.stripe_customer_id:
            return user.stripe_customer_id

        customer = stripe.Customer.create(
            email=user.email,
            name=f"{user.first_name} {user.last_name}",
            metadata={"user_id": str(user.id), "type": "catholic_ride_share_user"},
        )
        user.stripe_customer_id = customer["id"]
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.stripe_customer_id

    def get_ride_distance_miles(self, db: Session, *, ride_id: int) -> Optional[float]:
        """Estimate ride distance (straight line pickup→dropoff) in miles."""
        row = (
            db.query(
                func.ST_Distance(
                    RideRequest.pickup_location, RideRequest.destination_location
                ).label("meters")
            )
            .select_from(Ride)
            .join(RideRequest, RideRequest.id == Ride.ride_request_id)
            .filter(Ride.id == ride_id)
            .first()
        )
        if not row or row[0] is None:
            return None
        meters = float(row[0])
        return meters / 1609.34

    def create_donation_payment_intent(
        self,
        db: Session,
        *,
        amount_cents: int,
        donor: User,
        ride_id: int,
        driver_id: int,
        currency: str = "usd",
    ) -> DonationIntentResult:
        """Create a Stripe PaymentIntent and a pending Donation record."""
        if amount_cents < 100:
            raise ValueError("Donation amount must be at least $1.00.")
        if amount_cents > 100_000:
            raise ValueError("Donation amount must be <= $1,000.00.")

        customer_id = self.get_or_create_stripe_customer_id(db, user=donor)

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            customer=customer_id,
            automatic_payment_methods={"enabled": True},
            metadata={
                "type": "ride_donation",
                "ride_id": str(ride_id),
                "donor_id": str(donor.id),
                "driver_id": str(driver_id),
            },
            description=f"Donation for ride #{ride_id}",
        )

        donation = Donation(
            ride_id=ride_id,
            donor_id=donor.id,
            recipient_id=driver_id,
            amount_cents=amount_cents,
            currency=currency.upper(),
            stripe_payment_intent_id=intent["id"],
            stripe_client_secret=intent.get("client_secret"),
            stripe_status=intent["status"],
        )
        db.add(donation)
        db.commit()
        db.refresh(donation)

        client_secret = intent.get("client_secret")
        if not client_secret:
            raise RuntimeError("Stripe PaymentIntent missing client_secret.")

        return DonationIntentResult(
            payment_intent_id=intent["id"],
            client_secret=client_secret,
            amount_cents=amount_cents,
        )

    def verify_and_construct_event(self, *, payload: bytes, sig_header: str) -> Any:
        """Verify Stripe webhook signature and return the parsed event."""
        if not settings.STRIPE_WEBHOOK_SECRET:
            raise StripeNotConfiguredError(
                "Stripe webhook is not configured (STRIPE_WEBHOOK_SECRET)."
            )
        return stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)

    def handle_webhook_event(self, db: Session, *, event: Any) -> None:
        """Handle relevant Stripe webhook events and update Donation records."""
        event_type = event.get("type")
        data_object = event.get("data", {}).get("object", {})

        if event_type not in {
            "payment_intent.succeeded",
            "payment_intent.payment_failed",
            "payment_intent.canceled",
        }:
            return

        payment_intent_id = data_object.get("id")
        if not payment_intent_id:
            return

        donation = (
            db.query(Donation)
            .filter(Donation.stripe_payment_intent_id == payment_intent_id)
            .first()
        )

        if not donation:
            # Best-effort: create a donation record from metadata if we don't have one yet.
            metadata = data_object.get("metadata") or {}
            if metadata.get("type") != "ride_donation":
                return

            try:
                ride_id = int(metadata["ride_id"])
                donor_id = int(metadata["donor_id"])
                driver_id = int(metadata.get("driver_id") or 0) or None
            except (KeyError, ValueError):
                return

            donation = Donation(
                ride_id=ride_id,
                donor_id=donor_id,
                recipient_id=driver_id,
                amount_cents=int(data_object.get("amount") or 0),
                currency=str(data_object.get("currency") or "usd").upper(),
                stripe_payment_intent_id=payment_intent_id,
                stripe_status=str(data_object.get("status") or "pending"),
            )
            db.add(donation)

        donation.stripe_status = str(data_object.get("status") or donation.stripe_status)
        donation.stripe_charge_id = data_object.get("latest_charge") or donation.stripe_charge_id

        if event_type == "payment_intent.succeeded":
            donation.completed_at = donation.completed_at or datetime.utcnow()
            fee = self.calculate_stripe_fee_cents(donation.amount_cents)
            donation.stripe_fee_cents = fee
            donation.net_amount_cents = max(0, donation.amount_cents - fee)
        elif event_type in {"payment_intent.payment_failed", "payment_intent.canceled"}:
            donation.completed_at = donation.completed_at or datetime.utcnow()

        db.commit()
