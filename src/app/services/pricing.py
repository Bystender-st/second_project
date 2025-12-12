from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models import Package
from app.schemas.package import PackageResponse
from app.services.exchange_rate import get_usd_rate
from app.utils.package_presentation import compute_delivery_status


async def calculate_delivery_for_package(
    session: AsyncSession,
    session_id: str,
    package_id: int,
) -> Optional[PackageResponse]:
    """
    Рассчитывает стоимость доставки для одной посылки текущей сессии.
    Возвращает PackageResponse или None, если посылка не найдена.
    """

    # 1. Находим посылку, принадлежащую текущей сессии
    query = (
        select(Package)
        .options(joinedload(Package.type))
        .where(
            Package.id == package_id,
            Package.session_id == session_id,
        )
        .with_for_update()  # блокировка строки на время расчёта
    )
    result = await session.execute(query)
    pkg: Package | None = result.scalars().first()

    if pkg is None:
        return None

    if pkg.delivery_calculated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Стоимость доставки для этой посылки уже рассчитана.",
        )

    # 2. Получаем курс доллара
    usd_rate = await get_usd_rate()
    usd_rate_dec = Decimal(str(usd_rate))

    # 3. Считаем стоимость по формуле:
    # (вес в кг * 0.5 + стоимость содержимого * 0.01) * курс
    weight = Decimal(str(pkg.weight_kg))
    content_price = Decimal(str(pkg.content_price_usd))

    base = weight * Decimal("0.5") + content_price * Decimal("0.01")
    delivery_price = (base * usd_rate_dec).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    # 4. Обновляем запись
    pkg.delivery_price_rub = delivery_price
    pkg.delivery_calculated = True

    await session.commit()
    await session.refresh(pkg)

    # 5. Добавляем человекочитаемый статус стоимости
    pkg.delivery_status = compute_delivery_status(pkg)

    return PackageResponse.model_validate(pkg)
