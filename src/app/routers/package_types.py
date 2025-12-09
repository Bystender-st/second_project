from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.base import get_db
from app.db.models import PackageType
from app.schemas.package_type import PackageTypeResponse

router = APIRouter(prefix="/package-types", tags=["Package Types"])


@router.get("/", response_model=list[PackageTypeResponse])
async def get_package_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PackageType))
    types = result.scalars().all()
    return types
