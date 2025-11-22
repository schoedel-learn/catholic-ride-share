"""Authentication endpoints."""

from datetime import timedelta

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    EmailVerificationRequest,
    ForgotPasswordRequest,
    MessageResponse,
    ResendVerificationRequest,
    ResetPasswordRequest,
    ValidateResetTokenRequest,
)
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services import auth_email
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and send verification email."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Send verification email (best-effort; failures should not break registration)
    try:
        auth_email.send_verification_email(db_user)
    except Exception:
        # In production, log this exception; for now we silently ignore.
        pass

    return db_user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Login and get access token."""
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.id, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(subject=user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(payload: EmailVerificationRequest, db: Session = Depends(get_db)):
    """Verify a user's email address using a 6-digit code."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or code",
        )

    if user.is_verified:
        return MessageResponse(message="Email already verified")

    if not auth_email.verify_email_code(payload.email, payload.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or code",
        )

    user.is_verified = True
    db.commit()

    return MessageResponse(message="Email successfully verified")


@router.post("/resend-verification", response_model=MessageResponse)
def resend_verification(payload: ResendVerificationRequest, db: Session = Depends(get_db)):
    """Resend verification email to an unverified user."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        # Do not reveal whether the email exists
        return MessageResponse(message="If an account exists, a verification email was sent")

    if user.is_verified:
        return MessageResponse(message="Email already verified")

    try:
        auth_email.send_verification_email(user)
    except Exception:
        # Swallow errors to avoid leaking implementation details
        pass

    return MessageResponse(message="If an account exists, a verification email was sent")


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Initiate password reset by sending a reset token via email."""
    # Always return a generic message to avoid user enumeration.
    generic_message = (
        "If an account exists for this email, password reset instructions have been sent"
    )

    # Apply rate limiting based on the email identifier before checking existence.
    # Even when the limit is exceeded, we still return the generic message to avoid
    # revealing whether the email is registered.
    if not auth_email.can_request_password_reset(payload.email):
        return MessageResponse(message=generic_message)

    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return MessageResponse(message=generic_message)

    token = auth_email.create_password_reset_token(user)
    try:
        auth_email.send_password_reset_email(user, token)
    except Exception:
        # Do not leak failures to the client
        return MessageResponse(message=generic_message)

    return MessageResponse(message=generic_message)


@router.post("/validate-reset-token", response_model=MessageResponse)
def validate_reset_token(payload: ValidateResetTokenRequest):
    """Validate that a password reset token is still valid."""
    user_id = auth_email.get_user_id_from_reset_token(payload.token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    return MessageResponse(message="Token is valid")


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using a valid token."""
    user_id = auth_email.get_user_id_from_reset_token(payload.token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    user.password_hash = get_password_hash(payload.new_password)

    # Invalidate the token before committing the password change so it
    # cannot be reused if token invalidation fails.
    try:
        auth_email.invalidate_reset_token(payload.token)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not complete password reset. Please try again.",
        )

    # Commit the password change. If this fails after the token has been
    # invalidated, attempt to restore the token so the user can retry.
    try:
        db.commit()
    except Exception:
        db.rollback()
        try:
            auth_email.store_password_reset_token(user, payload.token)
        except Exception:
            # Best-effort restoration; if this fails, the user will need
            # to initiate a new password reset.
            pass

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not complete password reset. Please try again.",
        )

    return MessageResponse(message="Password has been reset successfully")
