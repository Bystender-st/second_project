from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.package import (
    PackageCreate,
    PackageResponse,
    PackageListResponse,
)
from app.services.package import (
    create_package,
    list_packages,
    get_package_by_id,
)
from app.utils.dependencies import get_session_id


router = APIRouter(tags=["Packages"])


@router.post(
    "/packages", response_model=PackageResponse, status_code=status.HTTP_201_CREATED
)
async def register_package(
    data: PackageCreate,
    db: AsyncSession = Depends(get_db),
    session_id: str = Depends(get_session_id),
):
    return await create_package(db, session_id, data)


@router.get("/packages", response_model=PackageListResponse)
async def get_packages(
    db: AsyncSession = Depends(get_db),
    session_id: str = Depends(get_session_id),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type_id: Optional[int] = Query(None),
    only_calculated: Optional[bool] = Query(
        None,
        description="Если true — только с рассчитанной стоимостью, если false — только без расчёта, если null — все",
    ),
):
    return await list_packages(
        session=db,
        session_id=session_id,
        page=page,
        page_size=page_size,
        type_id=type_id,
        only_calculated=only_calculated,
    )


@router.get("/packages/{package_id}", response_model=PackageResponse)
async def get_package(
    package_id: int,
    db: AsyncSession = Depends(get_db),
    session_id: str = Depends(get_session_id),
):
    pkg = await get_package_by_id(db, session_id, package_id)
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
        )
    return pkg
