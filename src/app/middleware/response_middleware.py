import json
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        response = await call_next(request)

        # Не трогаем ответы без тела
        if response.status_code == 204:
            return response

        content_type = response.headers.get("content-type", "")

        # Обрабатываем только JSON-ответы
        if "application/json" not in content_type:
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return response

        wrapped = {
            "success": True,
            "data": data,
        }

        return Response(
            content=json.dumps(wrapped, ensure_ascii=False),
            status_code=response.status_code,
            media_type="application/json",
        )
