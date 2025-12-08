import uuid
from fastapi import Request
from app.db.redis import get_redis

SESSION_COOKIE_NAME = "session_id"
SESSION_TTL_SECONDS = 60 * 60 * 24 * 7  # 7 дней


async def get_or_create_session_id(request: Request) -> str:
    redis = await get_redis()

    # 1. Пробуем получить session_id из cookie
    session_id = request.cookies.get(SESSION_COOKIE_NAME)

    if session_id:
        # Проверяем в Redis — существует ли он
        exists = await redis.exists(f"session:{session_id}")
        if exists:
            return session_id

    # 2. Создаём новый session_id
    session_id = uuid.uuid4().hex

    # Записываем в Redis, key = session:<id>
    await redis.set(f"session:{session_id}", "1", ex=SESSION_TTL_SECONDS)

    return session_id


async def bind_session_to_response(response, session_id: str):
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        samesite="lax",
        max_age=SESSION_TTL_SECONDS,
    )
