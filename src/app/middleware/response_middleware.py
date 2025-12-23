import json
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse

EXCLUDED_PATHS = {"/openapi.json", "/docs", "/redoc"}


class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        response = await call_next(request)

        # 1. Не трогаем системные эндпоинты FastAPI
        if request.url.path in EXCLUDED_PATHS:
            return response

        # 2. НЕ трогаем StreamingResponse (Swagger, файлы, SSE и т.д.)
        if isinstance(response, StreamingResponse):
            return response

        # 3. Не трогаем ответы без тела
        if response.status_code == 204:
            return response

        content_type = response.headers.get("content-type", "")

        # 4. Работаем только с JSON
        if "application/json" not in content_type:
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return response

        # 5. Error-ответы не оборачиваем
        if isinstance(data, dict) and data.get("success") is False:
            new_response = Response(
                content=json.dumps(data, ensure_ascii=False),
                status_code=response.status_code,
                media_type="application/json",
            )
        else:
            new_response = Response(
                content=json.dumps(
                    {"success": True, "data": data},
                    ensure_ascii=False,
                ),
                status_code=response.status_code,
                media_type="application/json",
            )

        # 6. Корректно переносим cookies
        for header, value in response.headers.items():
            if header.lower() == "set-cookie":
                new_response.headers.append("set-cookie", value)

        return new_response
