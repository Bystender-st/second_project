# src/app/db/base.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# settings.DATABASE_URL уже содержит строку вида mysql+aiomysql://...
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)

AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()


# Dependency for FastAPI endpoints later
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
