from fastapi import APIRouter, Query
from services.pagination_services import paginate
router = APIRouter(prefix="/demo", tags=["demo"])
@router.get("/items")
def get_demo_items(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    items = [{"id": i, "name": f"Item {i}"} for i in range(1, 201)]
    return paginate(items, limit=limit, offset=offset)