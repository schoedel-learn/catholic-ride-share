"""Redis client utilities."""

from functools import lru_cache

from redis import Redis

from app.core.config import settings


@lru_cache(maxsize=1)
def get_redis_client() -> Redis:
    """Get a cached Redis client instance."""
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis() -> Redis:
    """FastAPI-friendly dependency wrapper."""
    return get_redis_client()
