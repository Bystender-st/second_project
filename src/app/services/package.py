from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models import Package
from app.schemas.package import (
    PackageCreate,
    PackageResponse,
    PackageListResponse,
)
from app.utils.package_presentation import compute_delivery_status


async def create_package(
    session: AsyncSession,
    session_id: str,
    data: PackageCreate,
) -> PackageResponse:
    new_package = Package(
        session_id=session_id,
        name=data.name,
        weight_kg=data.weight_kg,
        type_id=data.type_id,
        content_price_usd=data.content_price_usd,
        delivery_calculated=False,
        delivery_price_rub=None,
        company_id=None,
    )

    session.add(new_package)
    await session.commit()
    await session.refresh(new_package)

    # подмешиваем вычисляемое поле
    new_package.delivery_status = compute_delivery_status(new_package)

    return PackageResponse.model_validate(new_package)


async def list_packages(
    session: AsyncSession,
    session_id: str,
    page: int,
    page_size: int,
    type_id: Optional[int] = None,
    only_calculated: Optional[bool] = None,
) -> PackageListResponse:
    base_query = (
        select(Package)
        .options(joinedload(Package.type))
        .where(Package.session_id == session_id)
    )

    if type_id is not None:
        base_query = base_query.where(Package.type_id == type_id)

    if only_calculated is not None:
        base_query = base_query.where(Package.delivery_calculated == only_calculated)

    # считаем total
    count_query = select(func.count()).select_from(base_query.subquery())
    total = await session.scalar(count_query)

    # пагинация
    offset = (page - 1) * page_size
    items_query = base_query.order_by(Package.id.desc()).offset(offset).limit(page_size)
    result = await session.execute(items_query)
    packages = result.scalars().all()

    # добавляем delivery_status каждому объекту
    for pkg in packages:
        pkg.delivery_status = compute_delivery_status(pkg)

    from app.schemas.package import PackageListItem  # во избежание циклов импорта

    return PackageListResponse(
        items=[PackageListItem.model_validate(p) for p in packages],
        total=total or 0,
        page=page,
        page_size=page_size,
    )


async def get_package_by_id(
    session: AsyncSession,
    session_id: str,
    package_id: int,
) -> Optional[PackageResponse]:
    query = (
        select(Package)
        .options(joinedload(Package.type))
        .where(
            Package.id == package_id,
            Package.session_id == session_id,
        )
    )
    result = await session.execute(query)
    pkg = result.scalars().first()
    if not pkg:
        return None

    pkg.delivery_status = compute_delivery_status(pkg)
    return PackageResponse.model_validate(pkg)
