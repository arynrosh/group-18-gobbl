from fastapi import APIRouter, Depends
from app.services.restaurant_service import search_by_name, search_by_cuisine
from app.schemas.pagination_schema import PaginationParams
from app.services.pagination_service import paginate
from typing import Dict, Any

router = APIRouter(prefix="/restaurant", tags=["restaurant"])

@router.get("/search/name", response_model=Dict[str, Any])
def search_restaurants_by_name(name: str, params: PaginationParams = Depends()):
    """
    Searches restaurants by name.

    Args:
        name (str): The name to search for.
        params (PaginationParams): Pagination parameters (limit, offset).

    Returns:
        Dict[str, Any]: Paginated list of matching restaurants.
    """
    results = search_by_name(name)
    return paginate(results, params.limit, params.offset)

@router.get("/search/cuisine", response_model=Dict[str, Any])
def search_restaurants_by_cuisine(cuisine: str, params: PaginationParams = Depends()):
    """
    Searches restaurants by cuisine type.

    Args:
        cuisine (str): The cuisine type to search for.
        params (PaginationParams): Pagination parameters (limit, offset).

    Returns:
        Dict[str, Any]: Paginated list of matching restaurants.
    """
    results = search_by_cuisine(cuisine)
    return paginate(results, params.limit, params.offset)
            