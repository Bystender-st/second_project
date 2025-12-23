from __future__ import annotations

from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status

from app.db.mongo import get_mongo_db


def _require_mongo():
    db = get_mongo_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB analytics is disabled or unavailable.",
        )
    return db


def _parse_tz_offset(tz_offset: str) -> timezone:
    """
    Часовой пояс: "+10:00", "-03:30", "+00:00"
    """
    try:
        sign = 1
        s = tz_offset.strip()
        if s[0] == "-":
            sign = -1
        if s[0] in "+-":
            s = s[1:]

        hh_str, mm_str = s.split(":")
        hh = int(hh_str)
        mm = int(mm_str)

        if not (0 <= hh <= 23 and 0 <= mm <= 59):
            raise ValueError

        return timezone(sign * timedelta(hours=hh, minutes=mm))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid tz_offset format. Use +HH:MM or -HH:MM.",
        ) from exc


def _parse_date_range(date: str, tz: timezone) -> tuple[datetime, datetime]:
    """
    Дата: 'ГГГГ-ММ-ДД' в часовом поясе.
    """
    try:
        local_start = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=tz)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid date format. Use YYYY-MM-DD.",
        ) from exc

    local_end = local_start + timedelta(days=1)

    return (
        local_start.astimezone(timezone.utc),
        local_end.astimezone(timezone.utc),
    )


async def get_daily_sum_by_type(
    *,
    date: str,
    tz_offset: str = "+00:00",
    limit: int = 100,
) -> list[dict]:
    db = _require_mongo()
    tz = _parse_tz_offset(tz_offset)
    start_utc, end_utc = _parse_date_range(date, tz)

    pipeline = [
        {
            "$match": {
                "calculated_at": {
                    "$gte": start_utc,
                    "$lt": end_utc,
                }
            }
        },
        {
            "$group": {
                "_id": "$type",
                "count": {"$sum": 1},
                "total_rub": {"$sum": "$delivery_price_rub"},
                "avg_rub": {"$avg": "$delivery_price_rub"},
            }
        },
        {"$sort": {"total_rub": -1}},
        {"$limit": limit},
        {
            "$project": {
                "_id": 0,
                "type": "$_id",
                "count": 1,
                "total_rub": 1,
                "avg_rub": 1,
            }
        },
    ]

    items = await db.delivery_calculations.aggregate(pipeline).to_list(length=limit)

    for it in items:
        it["type"] = it.get("type") or "unknown"
        it["count"] = int(it.get("count", 0))
        it["total_rub"] = float(it.get("total_rub", 0.0))
        it["avg_rub"] = float(it.get("avg_rub", 0.0))

    return items
