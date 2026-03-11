from fastapi import APIRouter
from app.services.menu_item_service import search_by_name, search_by_price_range
from app.schemas.menu_item import MenuItem
from typing import List

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/search/name", response_model=List[MenuItem])
def search_menu_items_by_name(name: str):
  
    return search_by_name(name)


@router.get("/search/price", response_model=List[MenuItem])
def search_menu_items_by_price(min_price: float, max_price: float):

    return search_by_price_range(min_price, max_price)