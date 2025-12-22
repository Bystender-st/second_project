import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.middleware.session_middleware import SessionMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.response_middleware import ResponseMiddleware
from app.routers.package_types import router as package_types_router
from app.routers.package import router as packages_router
from app.routers import debug
from app.routers.analytics import router as analytics_router
from app.scheduler.runner import init_scheduler
from app.errors.handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = None

    # В тестах scheduler не запускаем
    if os.getenv("DISABLE_SCHEDULER") != "1":
        scheduler = init_scheduler()

    yield

    if scheduler:
        scheduler.shutdown(wait=False)


app = FastAPI(
    title="Delivery Service",
    lifespan=lifespan,
)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Middleware
app.add_middleware(ResponseMiddleware)
app.add_middleware(SessionMiddleware)
app.add_middleware(LoggingMiddleware)

# Routers
app.include_router(package_types_router)
app.include_router(packages_router)
app.include_router(debug.router)
app.include_router(analytics_router)
