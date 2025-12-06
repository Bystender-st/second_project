from sqlalchemy import select
from app.db.models import PackageType
from app.db.base import AsyncSessionLocal  # ваше место сессий

DEFAULT_PACKAGE_TYPES = [
    {"name": "clothing"},
    {"name": "electronics"},
    {"name": "misc"},
]


async def seed_package_types():
    """
    Seed initial package types if they don't exist.
    Uses AsyncSessionLocal to operate with async SQLAlchemy.
    """
    async with AsyncSessionLocal() as session:
        # check existence
        result = await session.execute(select(PackageType))
        existing = result.scalars().all()
        if existing:
            return

        # create
        for item in DEFAULT_PACKAGE_TYPES:
            session.add(PackageType(**item))
        await session.commit()
