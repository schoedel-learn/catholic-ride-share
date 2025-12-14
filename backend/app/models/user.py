"""User model."""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from app.db.session import Base
from geoalchemy2 import Geography
from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserRole(str, enum.Enum):
    """User role enum."""

    RIDER = "rider"
    DRIVER = "driver"
    BOTH = "both"
    ADMIN = "admin"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    role: Mapped[str] = mapped_column(
        Enum("rider", "driver", "both", "admin", name="userrole"),
        default="rider",
        nullable=False,
    )

    parish_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    profile_photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Location tracking for drivers (PostGIS POINT: longitude, latitude)
    last_known_location: Mapped[Optional[Geography]] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=True
    )
    last_location_updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    driver_profile: Mapped["DriverProfile"] = relationship(
        "DriverProfile", back_populates="user", uselist=False
    )
