from fastapi import APIRouter, Depends
from app.services.menu_item_service import search_by_name
from app.schemas.pagination_schema import PaginationParams
from app.services.pagination_service import paginate
from typing import Dict, Any

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/search/name", response_model=Dict[str, Any])
def search_menu_items_by_name(name: str, params: PaginationParams = Depends()):
    """
    Searches menu items by name across all restaurants.

    Args:
        name (str): The name to search for.
        params (PaginationParams): Pagination parameters (limit, offset).

    Returns:
        Dict[str, Any]: Paginated list of matching menu items.
    """
    results = search_by_name(name)
    return paginate(results, params.limit, params.offset)
