"""Ride endpoints."""

from __future__ import annotations

from datetime import datetime

from app.api.deps.auth import get_current_verified_user
from app.db.session import get_db
from app.models.ride import Ride, RideStatus
from app.models.ride_request import RideRequest, RideRequestStatus
from app.models.user import User, UserRole
from app.schemas.ride import (
    RideAcceptResponse,
    RideRequestCreate,
    RideRequestResponse,
    RideStatusUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, status
from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session

router = APIRouter()


def _to_point(longitude: float, latitude: float) -> WKTElement:
    """Convert lat/long to PostGIS-compatible POINT."""
    return WKTElement(f"POINT({longitude} {latitude})", srid=4326)


def _ensure_driver(current_user: User) -> None:
    if current_user.role not in {UserRole.DRIVER, UserRole.BOTH, UserRole.ADMIN}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver access required to view or accept rides",
        )


@router.get("/mine", response_model=list[RideRequestResponse])
def list_my_ride_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """List ride requests created by the current user."""
    return (
        db.query(RideRequest)
        .filter(RideRequest.rider_id == current_user.id)
        .order_by(RideRequest.created_at.desc())
        .all()
    )


@router.get("/open", response_model=list[RideRequestResponse])
def list_open_requests_for_drivers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """List pending ride requests available for drivers to accept."""
    _ensure_driver(current_user)

    return (
        db.query(RideRequest)
        .filter(
            RideRequest.status == RideRequestStatus.PENDING,
            RideRequest.rider_id != current_user.id,
        )
        .order_by(RideRequest.created_at.desc())
        .all()
    )


@router.post("/", response_model=RideRequestResponse, status_code=status.HTTP_201_CREATED)
def create_ride_request(
    payload: RideRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """Create a new ride request."""
    ride_request = RideRequest(
        rider_id=current_user.id,
        destination_type=payload.destination_type,
        parish_id=payload.parish_id,
        pickup_location=_to_point(
            longitude=payload.pickup.longitude, latitude=payload.pickup.latitude
        ),
        destination_location=_to_point(
            longitude=payload.dropoff.longitude, latitude=payload.dropoff.latitude
        ),
        requested_datetime=payload.requested_datetime,
        notes=payload.notes,
        passenger_count=payload.passenger_count,
        status=RideRequestStatus.PENDING,
    )

    db.add(ride_request)
    db.commit()
    db.refresh(ride_request)

    return ride_request


@router.post(
    "/{ride_request_id}/accept",
    response_model=RideAcceptResponse,
    status_code=status.HTTP_201_CREATED,
)
def accept_ride_request(
    ride_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """Allow a driver to accept a pending ride request."""
    _ensure_driver(current_user)

    ride_request = db.query(RideRequest).filter(RideRequest.id == ride_request_id).first()
    if not ride_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride request not found")

    if ride_request.rider_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot accept your own ride request",
        )

    if ride_request.status != RideRequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride request is no longer available",
        )

    existing_ride = db.query(Ride).filter(Ride.ride_request_id == ride_request.id).first()
    if existing_ride:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride request already accepted",
        )

    ride = Ride(
        ride_request_id=ride_request.id,
        driver_id=current_user.id,
        rider_id=ride_request.rider_id,
        status=RideStatus.ACCEPTED,
        accepted_at=datetime.utcnow(),
    )

    ride_request.status = RideRequestStatus.ACCEPTED

    db.add(ride)
    db.commit()
    db.refresh(ride)

    return ride


@router.get("/assigned", response_model=list[RideAcceptResponse])
def list_assigned_rides(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """List rides assigned to the current driver."""
    _ensure_driver(current_user)
    return (
        db.query(Ride)
        .filter(Ride.driver_id == current_user.id)
        .order_by(Ride.accepted_at.desc())
        .all()
    )


@router.patch(
    "/{ride_id}/status",
    response_model=RideAcceptResponse,
)
def update_ride_status(
    ride_id: int,
    payload: RideStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user),
):
    """Update the status of an accepted ride (driver only)."""
    _ensure_driver(current_user)

    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found")

    if ride.driver_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your ride")

    ride.status = payload.status

    ride_request = db.query(RideRequest).filter(RideRequest.id == ride.ride_request_id).first()
    if ride_request:
        if payload.status in {RideStatus.DRIVER_ENROUTE, RideStatus.ARRIVED, RideStatus.PICKED_UP}:
            ride_request.status = RideRequestStatus.ACCEPTED
        elif payload.status == RideStatus.IN_PROGRESS:
            ride_request.status = RideRequestStatus.IN_PROGRESS
        elif payload.status == RideStatus.COMPLETED:
            ride_request.status = RideRequestStatus.COMPLETED
        elif payload.status == RideStatus.CANCELLED:
            ride_request.status = RideRequestStatus.CANCELLED

    db.commit()
    db.refresh(ride)

    return ride
