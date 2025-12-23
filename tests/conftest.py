import asyncio
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.main import app
from app.db.base import Base, get_session
from app.db.models import PackageType


# Test database (SQLite)

DATABASE_URL_TEST = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(
    DATABASE_URL_TEST,
    echo=False,
    future=True,
)

AsyncSessionTest = async_sessionmaker(
    engine_test,
    expire_on_commit=False,
)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionTest() as session:
        yield session


# Event loop (async tests)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Database setup


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="session", autouse=True)
async def seed_package_types(prepare_database):
    async with AsyncSessionTest() as session:
        session.add_all(
            [
                PackageType(id=1, name="clothing"),
                PackageType(id=2, name="electronics"),
                PackageType(id=3, name="misc"),
            ]
        )
        await session.commit()


# MOCK внешних сервисов


@pytest.fixture(autouse=True)
def mock_usd_rate(monkeypatch):
    async def fake_get_usd_rate():
        return 100.0  # фиксированный курс для тестов

    monkeypatch.setattr(
        "app.services.pricing.get_usd_rate",
        fake_get_usd_rate,
    )


# Test client


@pytest.fixture
def client(monkeypatch):
    # отключаем scheduler и redis в тестах
    monkeypatch.setenv("DISABLE_SCHEDULER", "1")
    monkeypatch.setenv("DISABLE_REDIS", "1")
    monkeypatch.setenv("DISABLE_MONGO", "1")

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
