from fastapi import APIRouter, Depends
from app.services.statistics_service import get_average_delivery_times
from app.auth.dependencies import require_roles

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/delivery-times")
def get_delivery_times(current_user: dict = Depends(require_roles("admin"))):
    """
    Returns average delivery delay per restaurant and system-wide average.
    Admin only. 
    """
    return get_average_delivery_times()