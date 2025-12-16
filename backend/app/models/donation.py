"""Donation model."""

from __future__ import annotations

from datetime import datetime

from app.db.session import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


class Donation(Base):
    """Donation tied to a completed ride (via Stripe PaymentIntent)."""

    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)

    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False, index=True)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    # Currently informational: the driver for the ride (future: tips / payouts).
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    amount_cents = Column(Integer, nullable=False)
    currency = Column(String, nullable=False, default="USD")

    stripe_payment_intent_id = Column(String, nullable=False, unique=True, index=True)
    # Stored so the rider can confirm payment after ride completion.
    stripe_client_secret = Column(String, nullable=True)
    stripe_charge_id = Column(String, nullable=True)
    stripe_status = Column(String, nullable=False, default="pending", index=True)

    stripe_fee_cents = Column(Integer, nullable=False, default=0)
    net_amount_cents = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
