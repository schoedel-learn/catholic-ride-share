"""User schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    phone: Optional[str] = None
    first_name: str
    last_name: str
    role: UserRole = UserRole.RIDER


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserUpdate(BaseModel):
    """User update schema."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    profile_photo_url: Optional[str] = None
    parish_id: Optional[int] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    parish_id: Optional[int] = None
    profile_photo_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
