from fastapi import APIRouter, Query

from app.services.analytics import get_daily_sum_by_type

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/daily-by-type",
    summary="Daily delivery cost summary by package type",
)
async def daily_by_type(
    date: str = Query(
        ...,
        description="Local date in format YYYY-MM-DD",
        example="2025-12-22",
    ),
    tz_offset: str = Query(
        "+00:00",
        description="Timezone offset (e.g. +10:00, -03:00)",
        example="+10:00",
    ),
    limit: int = Query(
        100,
        ge=1,
        le=500,
        description="Maximum number of types to return",
    ),
):
    items = await get_daily_sum_by_type(
        date=date,
        tz_offset=tz_offset,
        limit=limit,
    )

    return {
        "date": date,
        "tz_offset": tz_offset,
        "items": items,
    }
