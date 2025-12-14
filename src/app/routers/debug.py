from fastapi import APIRouter, status

from app.scheduler.tasks import process_pending_packages

router = APIRouter(
    prefix="/debug",
    tags=["debug"],
)


@router.post(
    "/run-delivery-calculation",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Manually trigger delivery price calculation job",
)
async def run_delivery_calculation():
    """
    Manually runs background delivery price calculation
    for all packages without calculated delivery cost.

    Intended for debugging and operational usage.
    """
    await process_pending_packages()
    return {
        "status": "accepted",
        "message": "Начата задача по расчету стоимости доставки.",
    }
