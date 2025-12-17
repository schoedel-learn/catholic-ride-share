"""Ride review model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Text

from app.db.session import Base


class RideReview(Base):
    """Rider's review of a completed ride (driver rating + optional comment)."""

    __tablename__ = "ride_reviews"

    id = Column(Integer, primary_key=True, index=True)

    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False, unique=True, index=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (Index("idx_driver_reviews", "reviewee_id", "rating"),)
