import os
import uuid
from fastapi import Request, Response

from app.db.redis import get_redis

SESSION_COOKIE_NAME = "session_id"
SESSION_TTL_SECONDS = 60 * 60 * 24 * 7  # 7 дней


async def get_or_create_session_id(request: Request) -> str:
    """
    Возвращает session_id из cookie или создаёт новый.
    В тестах Redis полностью отключён через DISABLE_REDIS=1.
    """

    session_id = request.cookies.get(SESSION_COOKIE_NAME)

    # В тестах Redis отключён — просто генерируем session_id
    if os.getenv("DISABLE_REDIS") == "1":
        return session_id or uuid.uuid4().hex

    redis = await get_redis()

    # Если session_id есть — проверяем, что он существует в Redis
    if session_id:
        exists = await redis.exists(f"session:{session_id}")
        if exists:
            return session_id

    # Иначе создаём новый
    session_id = uuid.uuid4().hex

    await redis.set(
        f"session:{session_id}",
        "1",
        ex=SESSION_TTL_SECONDS,
    )

    return session_id


async def bind_session_to_response(response: Response, session_id: str) -> None:
    """
    Привязывает session_id к HTTP-ответу через cookie.
    """

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        samesite="lax",
        max_age=SESSION_TTL_SECONDS,
    )
