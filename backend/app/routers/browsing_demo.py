from fastapi import APIRouter, Query
from services.pagination_service import paginate
from schemas.pagination_schemas import PaginationParams
router = APIRouter(prefix="/demo", tags=["demo"])
@router.get("/items")
def get_demo_items(pagination: PaginationParams = PaginationParams()):
    items = [{"id": i, "name": f"Item {i}"} for i in range(1, 201)]
    return paginate(items, limit=pagination.limit, offset=pagination.offset)