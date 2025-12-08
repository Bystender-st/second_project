from fastapi import FastAPI
from app.middleware.session_middleware import SessionMiddleware

app = FastAPI(title="Delivery Service")

# Подключаем middleware
app.add_middleware(SessionMiddleware)
