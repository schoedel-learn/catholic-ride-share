"""Donation and review endpoints (Stripe)."""

from __future__ import annotations

from datetime import datetime

from app.api.deps.auth import get_current_verified_user
from app.db.session import get_db
from app.models.donation import Donation
from app.models.ride import Ride, RideStatus
from app.models.ride_review import RideReview
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationIntentResponse,
    DonationPreferences,
    DonationPreferencesUpdate,
    DonationResponse,
    RideReviewCreate,
    RideReviewResponse,
)
from app.services.payment import PaymentService, StripeNotConfiguredError
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

router = APIRouter()


def _amount_to_cents(amount: float) -> int:
    return int(round(amount * 100))


def _donation_to_response(donation: Donation) -> DonationResponse:
    return DonationResponse.model_validate(
        {
            "id": donation.id,
            "ride_id": donation.ride_id,
            "amount": donation.amount_cents / 100.0,
            "currency": donation.currency,
            "stripe_status": donation.stripe_status,
            "created_at": donation.created_at,
            "completed_at": donation.completed_at,
            "stripe_fee_cents": donation.stripe_fee_cents,
            "net_amount_cents": donation.net_amount_cents,
        }
    )


def _prefs_to_response(user: User) -> DonationPreferences:
    return DonationPreferences.model_validate(
        {
            "auto_donation_enabled": user.auto_donation_enabled,
            "auto_donation_type": user.auto_donation_type,
            "auto_donation_amount": (
                (user.auto_donation_amount_cents / 100.0)
                if user.auto_donation_amount_cents
                else None
            ),
            "auto_donation_multiplier": user.auto_donation_multiplier,
        }
    )


@router.get("/users/me/donation-preferences", response_model=DonationPreferences)
def get_my_donation_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """Get the current user's auto-donation preferences."""
    _ = db  # keep signature consistent (db used for dependency lifecycle)
    return _prefs_to_response(current_user)


@router.put("/users/me/donation-preferences", response_model=DonationPreferences)
def update_my_donation_preferences(
    payload: DonationPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """Update the current user's auto-donation preferences."""
    new_type = payload.auto_donation_type or current_user.auto_donation_type

    if payload.auto_donation_enabled is not None:
        current_user.auto_donation_enabled = payload.auto_donation_enabled
    if payload.auto_donation_type is not None:
        current_user.auto_donation_type = payload.auto_donation_type

    if payload.auto_donation_amount is not None:
        current_user.auto_donation_amount_cents = _amount_to_cents(payload.auto_donation_amount)
    elif payload.auto_donation_type == "distance_based":
        # Switching to distance-based: fixed amount no longer applies.
        current_user.auto_donation_amount_cents = None

    if payload.auto_donation_multiplier is not None:
        current_user.auto_donation_multiplier = payload.auto_donation_multiplier
    elif payload.auto_donation_type == "fixed":
        # Switching to fixed: multiplier no longer applies.
        current_user.auto_donation_multiplier = None

    if (
        current_user.auto_donation_enabled
        and new_type == "fixed"
        and not current_user.auto_donation_amount_cents
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fixed auto-donation requires auto_donation_amount",
        )
    if current_user.auto_donation_enabled and new_type == "distance_based":
        # Provide a sensible default if user didn't set one yet.
        current_user.auto_donation_multiplier = current_user.auto_donation_multiplier or 0.5

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return _prefs_to_response(current_user)


@router.get("/users/me/donations", response_model=list[DonationResponse])
def list_my_donations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """List donations made by the current user."""
    donations = (
        db.query(Donation)
        .filter(Donation.donor_id == current_user.id)
        .order_by(Donation.created_at.desc())
        .all()
    )
    return [_donation_to_response(d) for d in donations]


@router.post(
    "/rides/{ride_id}/donate",
    response_model=DonationIntentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_manual_donation_intent(
    ride_id: int,
    payload: DonationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """Create a Stripe PaymentIntent for a donation on a completed ride."""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found")
    if ride.rider_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your ride")
    if ride.status != RideStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donations are only allowed after ride completion",
        )

    try:
        payment = PaymentService()
        intent = payment.create_donation_payment_intent(
            db,
            amount_cents=_amount_to_cents(payload.donation_amount),
            donor=current_user,
            ride_id=ride.id,
            driver_id=ride.driver_id,
        )
    except StripeNotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return DonationIntentResponse(
        payment_intent_id=intent.payment_intent_id,
        client_secret=intent.client_secret,
        amount=intent.amount_cents / 100.0,
        currency="USD",
    )


@router.post(
    "/rides/{ride_id}/review",
    response_model=RideReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_review_and_optional_donation(
    ride_id: int,
    payload: RideReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """Submit a ride review (and optional donation) for a completed ride."""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found")
    if ride.rider_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your ride")
    if ride.status != RideStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reviews are only allowed after ride completion",
        )

    existing_review = db.query(RideReview).filter(RideReview.ride_id == ride_id).first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride review already submitted",
        )

    donation_intent: DonationIntentResponse | None = None
    donation_response: DonationResponse | None = None

    if payload.donation_amount is not None:
        try:
            payment = PaymentService()
            intent = payment.create_donation_payment_intent(
                db,
                amount_cents=_amount_to_cents(payload.donation_amount),
                donor=current_user,
                ride_id=ride.id,
                driver_id=ride.driver_id,
            )
            donation = (
                db.query(Donation)
                .filter(Donation.stripe_payment_intent_id == intent.payment_intent_id)
                .first()
            )
            if donation:
                donation_response = _donation_to_response(donation)
            donation_intent = DonationIntentResponse(
                payment_intent_id=intent.payment_intent_id,
                client_secret=intent.client_secret,
                amount=intent.amount_cents / 100.0,
                currency="USD",
            )
        except StripeNotConfiguredError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
            ) from exc
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    review = RideReview(
        ride_id=ride.id,
        reviewer_id=current_user.id,
        reviewee_id=ride.driver_id,
        rating=payload.rating,
        comment=payload.comment,
        created_at=datetime.utcnow(),
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    return RideReviewResponse(
        id=review.id,
        ride_id=review.ride_id,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at,
        donation=donation_response,
        donation_intent=donation_intent,
    )


@router.get("/rides/{ride_id}/donation-intent", response_model=DonationIntentResponse)
def get_latest_donation_intent_for_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """Fetch the most recent donation PaymentIntent (client_secret) for a ride."""
    donation = (
        db.query(Donation)
        .filter(Donation.ride_id == ride_id, Donation.donor_id == current_user.id)
        .order_by(Donation.created_at.desc())
        .first()
    )
    if not donation or not donation.stripe_client_secret:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Donation intent not found"
        )

    return DonationIntentResponse(
        payment_intent_id=donation.stripe_payment_intent_id,
        client_secret=donation.stripe_client_secret,
        amount=donation.amount_cents / 100.0,
        currency=donation.currency,
    )


@router.post("/webhooks/stripe", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(default="", alias="Stripe-Signature"),
    db: Session = Depends(get_db),
):
    """Handle Stripe webhook events."""
    payload = await request.body()

    try:
        payment = PaymentService()
        event = payment.verify_and_construct_event(payload=payload, sig_header=stripe_signature)
        payment.handle_webhook_event(db, event=event)
    except StripeNotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    except ValueError as exc:
        # Invalid payload
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {"received": True}
