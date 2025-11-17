"""Driver endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter()


@router.get("/available")
def get_available_drivers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get available drivers nearby."""
    # TODO: Implement driver discovery
    return {"message": "Available drivers endpoint - to be implemented"}


@router.post("/profile")
def create_driver_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create driver profile."""
    # TODO: Implement driver profile creation
    return {"message": "Create driver profile endpoint - to be implemented"}
