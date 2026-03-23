from fastapi import APIRouter, Depends
from app.schemas.pagination_schema import PaginationParams
from app.services.pagination_service import paginate
from app.services.restaurant_service import restaurants
from typing import Dict, Any

router = APIRouter(prefix="/browse", tags=["browse"])

@router.get("/restaurants", response_model=Dict[str, Any])
def browse_restaurants(params: PaginationParams = Depends()):
    """
    Returns paginated list of restaurants.
    """
    return paginate(restaurants, params.limit, params.offset)