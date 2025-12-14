from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.error import ErrorResponse, ErrorDetails


def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorDetails(
            code="http_error",
            message=str(exc.detail),
        )
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # Сводим pydantic-ошибки в человекочитаемую строку (минимально инвазивно)
    msg = "Validation error"
    if exc.errors():
        first = exc.errors()[0]
        loc = ".".join(str(x) for x in first.get("loc", []))
        detail = first.get("msg", "")
        msg = f"{loc}: {detail}".strip(": ")

    payload = ErrorResponse(
        error=ErrorDetails(
            code="validation_error",
            message=msg,
        )
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorDetails(
            code="internal_error",
            message="Internal server error",
        )
    )
    return JSONResponse(status_code=500, content=payload.model_dump())
