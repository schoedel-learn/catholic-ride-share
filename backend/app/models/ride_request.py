"""Ride request model."""

import enum
from datetime import datetime

from app.db.session import Base
from geoalchemy2 import Geography
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text


class DestinationType(str, enum.Enum):
    """Destination type enum."""

    MASS = "mass"
    CONFESSION = "confession"
    PRAYER_EVENT = "prayer_event"
    SOCIAL = "social"
    OTHER = "other"


class RideRequestStatus(str, enum.Enum):
    """Ride request status enum."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RideRequest(Base):
    """Ride request model."""

    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Destination info
    destination_type = Column(
        Enum("mass", "confession", "prayer_event", "social", "other", name="destinationtype"),
        nullable=False,
    )
    parish_id = Column(Integer, ForeignKey("parishes.id"), nullable=True)

    # Locations (using PostGIS)
    pickup_location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    destination_location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    # Timing
    requested_datetime = Column(DateTime, nullable=False)

    # Additional info
    notes = Column(Text, nullable=True)
    passenger_count = Column(Integer, default=1, nullable=False)

    # Status
    status = Column(
        Enum(
            "pending", "accepted", "in_progress", "completed", "cancelled", name="riderequeststatus"
        ),
        default="pending",
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
