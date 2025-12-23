from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import os

_client: AsyncIOMotorClient | None = None


def get_mongo_client() -> AsyncIOMotorClient | None:
    if os.getenv("DISABLE_MONGO") == "1":
        return None

    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URL)

    return _client


def get_mongo_db():
    client = get_mongo_client()
    if client is None:
        return None

    return client[settings.MONGO_DB_NAME]
