"""Ride model."""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from geoalchemy2 import Geography
import enum

from app.db.session import Base


class RideStatus(str, enum.Enum):
    """Ride status enum."""
    ACCEPTED = "accepted"
    DRIVER_ENROUTE = "driver_enroute"
    ARRIVED = "arrived"
    PICKED_UP = "picked_up"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Ride(Base):
    """Ride model."""

    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    ride_request_id = Column(Integer, ForeignKey("ride_requests.id"), nullable=False, unique=True)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rider_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Timing
    accepted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    pickup_time = Column(DateTime, nullable=True)
    dropoff_time = Column(DateTime, nullable=True)

    # Actual locations (may differ slightly from requested)
    actual_pickup_location = Column(Geography(geometry_type='POINT', srid=4326), nullable=True)
    actual_dropoff_location = Column(Geography(geometry_type='POINT', srid=4326), nullable=True)

    # Status
    status = Column(Enum(RideStatus), default=RideStatus.ACCEPTED, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
