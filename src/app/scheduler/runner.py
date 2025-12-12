from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.scheduler.tasks import process_pending_packages


def init_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        process_pending_packages,
        "interval",
        minutes=5,
        id="delivery_price_recalculation",
        replace_existing=True,
    )

    scheduler.start()
    return scheduler
