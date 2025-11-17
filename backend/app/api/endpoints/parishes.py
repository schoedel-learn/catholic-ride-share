"""Parish endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("/")
def list_parishes(db: Session = Depends(get_db)):
    """List all parishes."""
    # TODO: Implement parish listing
    return {"message": "List parishes endpoint - to be implemented"}


@router.get("/{parish_id}")
def get_parish(parish_id: int, db: Session = Depends(get_db)):
    """Get parish by ID."""
    # TODO: Implement parish retrieval
    return {"message": f"Get parish {parish_id} endpoint - to be implemented"}
