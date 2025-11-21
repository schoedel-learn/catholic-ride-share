"""Authentication-related schemas (email verification and password reset)."""

from pydantic import BaseModel, EmailStr, Field


class EmailVerificationRequest(BaseModel):
    """Request body for verifying email with a code."""

    email: EmailStr
    code: str = Field(min_length=6, max_length=6)


class ResendVerificationRequest(BaseModel):
    """Request body for resending verification email."""

    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    """Request body for initiating a password reset."""

    email: EmailStr


class ValidateResetTokenRequest(BaseModel):
    """Request body for validating a password reset token."""

    token: str


class ResetPasswordRequest(BaseModel):
    """Request body for resetting password with a token."""

    token: str
    new_password: str = Field(min_length=8)


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str


