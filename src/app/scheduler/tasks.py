from sqlalchemy import select

from app.db.base import AsyncSessionLocal
from app.db.models import Package
from app.services.pricing import calculate_delivery_for_package


async def process_pending_packages():
    """Обрабатывает все посылки, у которых не рассчитана доставка."""
    async with AsyncSessionLocal() as session:
        query = select(Package).where(Package.delivery_calculated.is_(False))

        result = await session.execute(query)
        pending_packages = result.scalars().all()

        if not pending_packages:
            return

        for pkg in pending_packages:
            await calculate_delivery_for_package(
                session=session,
                session_id=pkg.session_id,  # расчёт привязан к сессии
                package_id=pkg.id,
            )
