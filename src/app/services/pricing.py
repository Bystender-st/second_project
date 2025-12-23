from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, cast

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models import Package
from app.schemas.package import PackageResponse
from app.services.exchange_rate import get_usd_rate
from app.services.delivery_log import log_delivery_calculation
from app.utils.package_presentation import compute_delivery_status


async def calculate_delivery_for_package(
    session: AsyncSession,
    session_id: str,
    package_id: int,
) -> Optional[PackageResponse]:
    """
    Рассчитывает стоимость доставки для одной посылки текущей сессии.
    """

    query = (
        select(Package)
        .options(joinedload(Package.type))
        .where(
            Package.id == package_id,
            Package.session_id == session_id,
        )
        .with_for_update()
    )

    result = await session.execute(query)
    pkg: Package | None = result.scalars().first()

    if pkg is None:
        return None

    if cast(bool, pkg.delivery_calculated):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Стоимость доставки для этой посылки уже рассчитана.",
        )

    usd_rate = await get_usd_rate()
    usd_rate_dec = Decimal(str(usd_rate))

    weight = Decimal(str(pkg.weight_kg))
    content_price = Decimal(str(pkg.content_price_usd))

    base = weight * Decimal("0.5") + content_price * Decimal("0.01")
    delivery_price = (base * usd_rate_dec).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    pkg.delivery_price_rub = cast(Decimal, delivery_price)
    pkg.delivery_calculated = cast(bool, True)

    await session.commit()
    await session.refresh(pkg)

    pkg.delivery_status = compute_delivery_status(pkg)

    try:
        await log_delivery_calculation(
            package_id=pkg.id,
            session_id=session_id,
            weight_kg=float(pkg.weight_kg),
            type_name=pkg.type.name if pkg.type else "unknown",
            content_price_usd=float(pkg.content_price_usd),
            usd_rate=float(usd_rate),
            delivery_price_rub=float(pkg.delivery_price_rub),
        )
    except Exception:
        pass

    return PackageResponse.model_validate(pkg)
