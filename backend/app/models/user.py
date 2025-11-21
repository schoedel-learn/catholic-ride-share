"""User model."""

from datetime import datetime
import enum

from geoalchemy2 import Geography
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class UserRole(str, enum.Enum):
    """User role enum."""
    RIDER = "rider"
    DRIVER = "driver"
    BOTH = "both"
    ADMIN = "admin"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.RIDER, nullable=False)

    parish_id = Column(Integer, nullable=True)
    profile_photo_url = Column(String, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Location tracking for drivers (PostGIS POINT: longitude, latitude)
    last_known_location = Column(
        Geography(geometry_type="POINT", srid=4326), nullable=True
    )
    last_location_updated_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    driver_profile = relationship("DriverProfile", back_populates="user", uselist=False)
