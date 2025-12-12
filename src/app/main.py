from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.middleware.session_middleware import SessionMiddleware
from app.routers.package_types import router as package_types_router
from app.routers.package import router as packages_router
from app.scheduler.runner import init_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = init_scheduler()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(title="Delivery Service", lifespan=lifespan)

# Middleware
app.add_middleware(SessionMiddleware)

# Routers
app.include_router(package_types_router)

app.include_router(packages_router)
