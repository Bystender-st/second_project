import httpx

from app.db.redis import get_redis
from app.config import settings


CACHE_KEY = "usd_rate"
CACHE_TTL = 600  # 10 минут


async def fetch_usd_from_cbr() -> float:
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(settings.CBR_URL)
        response.raise_for_status()
        data = response.json()
        return float(data["Valute"]["USD"]["Value"])


async def get_usd_rate() -> float:
    redis = await get_redis()

    # 1. Пробуем получить из Redis
    cached_value = await redis.get(CACHE_KEY)
    if cached_value is not None:
        return float(cached_value)

    # 2. Идём в API CBR
    try:
        rate = await fetch_usd_from_cbr()
    except Exception:
        if cached_value is not None:
            return float(cached_value)
        raise RuntimeError("Не удалось получить курс USD ни из API, ни из кеша")

    # 3. Кладём в Redis
    await redis.set(CACHE_KEY, rate, ex=CACHE_TTL)

    return rate
