"""Email verification and password reset services."""

from __future__ import annotations

import secrets
from datetime import timedelta

from redis import Redis

from app.core.redis import get_redis_client
from app.models.user import User
from app.services.email import send_email

EMAIL_VERIFICATION_PREFIX = "email_verification"
PASSWORD_RESET_PREFIX = "password_reset"
PASSWORD_RESET_RATE_PREFIX = "password_reset_rate"

EMAIL_VERIFICATION_TTL = timedelta(hours=24)
PASSWORD_RESET_TTL = timedelta(hours=1)
PASSWORD_RESET_RATE_WINDOW = timedelta(hours=1)
PASSWORD_RESET_RATE_LIMIT = 3


def _build_key(prefix: str, identifier: str) -> str:
    return f"{prefix}:{identifier}"


def _get_redis() -> Redis:
    return get_redis_client()


def generate_verification_code() -> str:
    """Generate a 6-digit numeric verification code."""
    return f"{secrets.randbelow(1_000_000):06d}"


def send_verification_email(user: User) -> None:
    """Generate and send an email verification code to the user."""
    redis = _get_redis()
    code = generate_verification_code()
    key = _build_key(EMAIL_VERIFICATION_PREFIX, user.email)

    redis.setex(key, int(EMAIL_VERIFICATION_TTL.total_seconds()), code)

    subject = "Verify your Catholic Ride Share account"
    body = (
        f"Hello {user.first_name},\n\n"
        f"Your email verification code is: {code}\n\n"
        "This code will expire in 24 hours.\n\n"
        "If you did not create this account, you can ignore this email.\n"
    )

    send_email(to_email=user.email, subject=subject, body=body)


def verify_email_code(email: str, code: str) -> bool:
    """Verify that the provided code matches the stored verification code."""
    redis = _get_redis()
    key = _build_key(EMAIL_VERIFICATION_PREFIX, email)
    stored = redis.get(key)

    if stored is None or stored != code:
        return False

    redis.delete(key)
    return True


def generate_password_reset_token() -> str:
    """Generate a secure password reset token."""
    return secrets.token_urlsafe(32)


def _increment_rate_limit(email: str) -> int:
    """Increment and return the password reset request count for this email."""
    redis = _get_redis()
    key = _build_key(PASSWORD_RESET_RATE_PREFIX, email.lower())

    # INCR followed by setting expiry if key is new
    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, int(PASSWORD_RESET_RATE_WINDOW.total_seconds()))
    count, _ = pipe.execute()
    return int(count)


def can_request_password_reset(email: str) -> bool:
    """Check if password reset can be requested under rate limits."""
    count = _increment_rate_limit(email)
    return count <= PASSWORD_RESET_RATE_LIMIT


def create_password_reset_token(user: User) -> str:
    """Create and store a password reset token for the given user."""
    token = generate_password_reset_token()
    redis = _get_redis()
    key = _build_key(PASSWORD_RESET_PREFIX, token)

    redis.setex(key, int(PASSWORD_RESET_TTL.total_seconds()), str(user.id))
    return token


def send_password_reset_email(user: User, token: str) -> None:
    """Send password reset email with the given token."""
    subject = "Reset your Catholic Ride Share password"
    body = (
        f"Hello {user.first_name},\n\n"
        "A request was received to reset your Catholic Ride Share password.\n\n"
        f"Your password reset token is:\n\n{token}\n\n"
        "This token will expire in 1 hour.\n\n"
        "If you did not request a password reset, you can ignore this email.\n"
    )

    send_email(to_email=user.email, subject=subject, body=body)


def get_user_id_from_reset_token(token: str) -> int | None:
    """Return the user ID associated with the reset token, or None if invalid/expired."""
    redis = _get_redis()
    key = _build_key(PASSWORD_RESET_PREFIX, token)
    value = redis.get(key)
    return int(value) if value is not None else None


def invalidate_reset_token(token: str) -> None:
    """Invalidate a used password reset token."""
    redis = _get_redis()
    key = _build_key(PASSWORD_RESET_PREFIX, token)
    redis.delete(key)


