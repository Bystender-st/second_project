from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Package
from app.schemas.package import PackageCreate, PackageResponse


async def create_package(
    session: AsyncSession, session_id: str, data: PackageCreate
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

    return PackageResponse.model_validate(new_package)
