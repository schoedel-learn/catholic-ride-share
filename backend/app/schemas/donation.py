"""Schemas for donations and ride reviews."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

AutoDonationType = Literal["fixed", "distance_based"]


class DonationCreate(BaseModel):
    """Request to donate for a ride."""

    donation_amount: float = Field(..., ge=1.00, le=1000.00, description="USD amount (dollars)")


class DonationIntentResponse(BaseModel):
    """Stripe PaymentIntent details needed by the client."""

    payment_intent_id: str
    client_secret: str
    amount: float
    currency: str


class DonationResponse(BaseModel):
    """Donation record response."""

    id: int
    ride_id: int
    amount: float
    currency: str
    stripe_status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    stripe_fee_cents: int
    net_amount_cents: int

    class Config:
        from_attributes = True


class DonationPreferences(BaseModel):
    """User donation preference response."""

    auto_donation_enabled: bool
    auto_donation_type: AutoDonationType
    auto_donation_amount: Optional[float] = None  # USD, only for fixed
    auto_donation_multiplier: Optional[float] = None  # USD per mile, only for distance_based


class DonationPreferencesUpdate(BaseModel):
    """Update user donation preferences."""

    auto_donation_enabled: Optional[bool] = None
    auto_donation_type: Optional[AutoDonationType] = None
    auto_donation_amount: Optional[float] = Field(default=None, ge=1.00, le=1000.00)
    auto_donation_multiplier: Optional[float] = Field(default=None, ge=0.01, le=50.0)


class RideReviewCreate(BaseModel):
    """Create a ride review and optional donation."""

    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=500)
    donation_amount: Optional[float] = Field(default=None, ge=1.00, le=1000.00)


class RideReviewResponse(BaseModel):
    """Ride review response with optional donation."""

    id: int
    ride_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    donation: Optional[DonationResponse] = None
    donation_intent: Optional[DonationIntentResponse] = None

    class Config:
        from_attributes = True
