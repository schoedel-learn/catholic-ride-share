"""Simple Redis-backed rate limiting utilities."""

from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, status

from app.core.redis import get_redis_client


def check_rate_limit(
    key: str,
    limit: int,
    window_seconds: int,
    error_message: Optional[str] = None,
) -> None:
    """Increment rate counter and raise if over limit.

    Args:
        key: Identifier (e.g., email or ip+email) used as the Redis key suffix.
        limit: Max allowed hits within the window.
        window_seconds: Rolling window in seconds.
        error_message: Optional custom message for the 429 response.
    """
    redis = get_redis_client()
    redis_key = f"ratelimit:{key}"

    # Pipeline to increment and set expiry atomically.
    pipeline = redis.pipeline()
    pipeline.incr(redis_key)
    pipeline.expire(redis_key, window_seconds)
    current, _ = pipeline.execute()

    if int(current) > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_message or "Too many requests, please try again later.",
        )
