from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_session
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
from app.services.pricing import calculate_delivery_for_package
from app.utils.dependencies import get_session_id
from app.utils.session import get_or_create_session_id

router = APIRouter(tags=["Packages"])


@router.post(
    "/packages",
    response_model=PackageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_package(
    data: PackageCreate,
    session: AsyncSession = Depends(get_session),
    session_id: str = Depends(get_session_id),
):
    return await create_package(session, session_id, data)


@router.get("/packages", response_model=PackageListResponse)
async def get_packages(
    session: AsyncSession = Depends(get_session),
    session_id: str = Depends(get_session_id),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type_id: Optional[int] = Query(None),
    only_calculated: Optional[bool] = Query(
        None,
        description=(
            "Если true — только с рассчитанной стоимостью, "
            "если false — только без расчёта, если null — все"
        ),
    ),
):
    return await list_packages(
        session=session,
        session_id=session_id,
        page=page,
        page_size=page_size,
        type_id=type_id,
        only_calculated=only_calculated,
    )


@router.get("/packages/{package_id}", response_model=PackageResponse)
async def get_package(
    package_id: int,
    session: AsyncSession = Depends(get_session),
    session_id: str = Depends(get_session_id),
):
    pkg = await get_package_by_id(session, session_id, package_id)
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Посылка не найдена.",
        )
    return pkg


@router.post(
    "/packages/{package_id}/calculate",
    response_model=PackageResponse,
)
async def calculate_delivery(
    package_id: int,
    session: AsyncSession = Depends(get_session),
    session_id: str = Depends(get_or_create_session_id),
):
    result = await calculate_delivery_for_package(
        session=session,
        session_id=session_id,
        package_id=package_id,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Посылка не найдена или не принадлежит вашей сессии.",
        )

    return result
