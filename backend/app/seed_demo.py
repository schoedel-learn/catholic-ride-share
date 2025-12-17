"""Seed demo data for local/testing environments."""

from __future__ import annotations

from datetime import datetime, timedelta

from geoalchemy2 import WKTElement

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.parish import Parish
from app.models.ride import Ride
from app.models.ride_request import RideRequest
from app.models.user import User


def _get_or_create_parish(session, name: str, city: str = "Springfield") -> Parish:
    parish = session.query(Parish).filter(Parish.name == name).first()
    if parish:
        return parish

    parish = Parish(
        name=name,
        address_line1="123 Church St",
        city=city,
        state="IL",
        zip_code="62701",
    )
    session.add(parish)
    session.commit()
    session.refresh(parish)
    return parish


def _get_or_create_user(session, email: str, role: str, first: str, last: str) -> User:
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user

    user = User(
        email=email,
        phone=None,
        password_hash=get_password_hash("Password123!"),
        first_name=first,
        last_name=last,
        role=role,  # Pass string value directly
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def _point(lon: float, lat: float) -> WKTElement:
    return WKTElement(f"POINT({lon} {lat})", srid=4326)


def seed() -> None:
    """Seed demo parishes, users, and rides."""
    session = SessionLocal()

    try:
        parish_st_mary = _get_or_create_parish(session, "St. Mary Parish")
        parish_st_joseph = _get_or_create_parish(session, "St. Joseph Parish")

        rider = _get_or_create_user(
            session,
            email="rider.demo@example.com",
            role="rider",
            first="Demo",
            last="Rider",
        )
        driver = _get_or_create_user(
            session,
            email="driver.demo@example.com",
            role="driver",
            first="Demo",
            last="Driver",
        )

        # Ensure there is at least one pending and one accepted ride request
        existing_requests = session.query(RideRequest).count()
        if existing_requests < 2:
            pending_request = RideRequest(
                rider_id=rider.id,
                destination_type="mass",
                parish_id=parish_st_mary.id,
                pickup_location=_point(-122.4194, 37.7749),
                destination_location=_point(-122.4094, 37.7849),
                requested_datetime=datetime.utcnow() + timedelta(hours=3),
                notes="Sunday Mass ride",
                passenger_count=2,
                status="pending",
            )
            session.add(pending_request)

            accepted_request = RideRequest(
                rider_id=rider.id,
                destination_type="prayer_event",
                parish_id=parish_st_joseph.id,
                pickup_location=_point(-122.3894, 37.7649),
                destination_location=_point(-122.3994, 37.7749),
                requested_datetime=datetime.utcnow() + timedelta(hours=1),
                notes="Rosary group meetup",
                passenger_count=1,
                status="accepted",
            )
            session.add(accepted_request)
            session.commit()
            session.refresh(accepted_request)

            existing_ride = (
                session.query(Ride).filter(Ride.ride_request_id == accepted_request.id).first()
            )
            if not existing_ride:
                ride = Ride(
                    ride_request_id=accepted_request.id,
                    driver_id=driver.id,
                    rider_id=rider.id,
                    status="accepted",
                    accepted_at=datetime.utcnow(),
                )
                session.add(ride)

        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    seed()
