import logging
from datetime import datetime, UTC

from app.db.mongo import get_mongo_db

logger = logging.getLogger("app.mongo")


async def log_delivery_calculation(
    *,
    package_id: int,
    session_id: str,
    weight_kg: float,
    type_name: str,
    content_price_usd: float,
    usd_rate: float,
    delivery_price_rub: float,
) -> None:
    db = get_mongo_db()
    if db is None:
        return

    try:
        await db.delivery_calculations.insert_one(
            {
                "package_id": package_id,
                "session_id": session_id,
                "weight_kg": weight_kg,
                "type": type_name,
                "content_price_usd": content_price_usd,
                "usd_rate": usd_rate,
                "delivery_price_rub": delivery_price_rub,
                "calculated_at": datetime.now(UTC),
            }
        )
    except Exception:
        logger.exception("Mongo logging failed")
