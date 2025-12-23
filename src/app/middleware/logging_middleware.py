import time
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.request")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        start_time = time.perf_counter()

        response: Response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000

        session_id = request.cookies.get("session_id")

        logger.info(
            "HTTP request handled",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration, 2),
                "session_id": session_id,
            },
        )

        return response
