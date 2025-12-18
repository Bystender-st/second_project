from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.base import get_session
from app.db.models import PackageType
from app.schemas.package_type import PackageTypeResponse

router = APIRouter(prefix="/package-types", tags=["Package Types"])


@router.get("/", response_model=list[PackageTypeResponse])
async def get_package_types(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(PackageType))
    return result.scalars().all()
