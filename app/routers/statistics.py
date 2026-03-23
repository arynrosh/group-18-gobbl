from fastapi import APIRouter
from app.services.statistics_service import get_average_delivery_times

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/delivery-times")
def get_delivery_times():
    """
    Returns average delivery delay per restaurant and system-wide average.
    """
    return get_average_delivery_times()