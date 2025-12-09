from typing import Optional
import redis.asyncio as redis
from redis.asyncio import Redis

from app.config import settings

_redis: Optional[Redis] = None


async def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis
