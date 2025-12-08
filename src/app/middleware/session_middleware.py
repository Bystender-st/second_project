from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.session import get_or_create_session_id, bind_session_to_response


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Получаем или создаём session_id
        session_id = await get_or_create_session_id(request)

        # Сохраняем в request.state.session_id
        request.state.session_id = session_id

        # Обрабатываем запрос
        response = await call_next(request)

        # Привязываем cookie к ответу
        await bind_session_to_response(response, session_id)

        return response
