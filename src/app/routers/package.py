from fastapi import APIRouter, Depends

from app.db.base import get_db
from app.schemas.package import PackageCreate, PackageResponse
from app.services.package import create_package
from app.utils.session import get_or_create_session_id

router = APIRouter(tags=["Packages"])


@router.post("/packages", response_model=PackageResponse)
async def register_package(
    data: PackageCreate,
    session_id: str = Depends(get_or_create_session_id),
    db=Depends(get_db),
):
    return await create_package(db, session_id, data)
