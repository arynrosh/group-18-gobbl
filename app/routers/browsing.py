from fastapi import APIRouter
from app.services.restaurant_service import search_by_name, search_by_cuisine
from app.services.pagination_service import paginate
from app.schemas.pagination_schema import PaginationParams

router = APIRouter(prefix="/browse", tags=["browse"])

@router.get("/restaurants/name")
def search_restaurants_by_name(name: str, pagination: PaginationParams = PaginationParams()):
    results = search_by_name(name)
    return paginate([r.dict() for r in results], limit=pagination.limit, offset=pagination.offset)

@router.get("/restaurants/cuisine")
def search_restaurants_by_cuisine(cuisine: str, pagination: PaginationParams = PaginationParams()):
    results = search_by_cuisine(cuisine)
    return paginate([r.dict() for r in results], limit=pagination.limit, offset=pagination.offset)