from fastapi import FastAPI
from app.middleware.session_middleware import SessionMiddleware
from app.routers.package_types import router as package_types_router

app = FastAPI(title="Delivery Service")

# Подключаем middleware
app.add_middleware(SessionMiddleware)

# Routers
app.include_router(package_types_router)
