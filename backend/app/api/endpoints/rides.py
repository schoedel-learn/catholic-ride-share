"""Ride endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter()


@router.get("/")
def list_rides(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List rides for current user."""
    # TODO: Implement ride listing
    return {"message": "List rides endpoint - to be implemented"}


@router.post("/")
def create_ride_request(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new ride request."""
    # TODO: Implement ride request creation
    return {"message": "Create ride request endpoint - to be implemented"}
