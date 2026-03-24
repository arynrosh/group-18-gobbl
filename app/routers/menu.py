from fastapi import APIRouter, Depends, Query, status
from typing import Optional

from app.auth.dependencies import require_roles
from app.schemas.menu import MenuItemCreate, MenuItemUpdate
from app.services import menu_service

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/{restaurant_id}")
def list_menu_items(
    restaurant_id: int,
    price_tier: Optional[str] = Query(None, pattern=r"^\${1,4}$"),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
):

    return menu_service.list_menu_items(
        restaurant_id, 
        price_tier, 
        min_rating,
    )

@router.post("/{restaurant_id}", status_code=status.HTTP_201_CREATED)
def create_menu_item(
    restaurant_id: int,
    item_data: MenuItemCreate,
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    
    item = menu_service.create_menu_item(
        restaurant_id,
        item_data
    )

    return {"message": "Menu item created", "item": item}

@router.put("/{restaurant_id}/{menu_id}")
def update_menu_item(
    restaurant_id: int,
    menu_id: int,
    item_data: MenuItemUpdate,
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    item = menu_service.update_menu_item(
        restaurant_id,
        menu_id,
        item_data
        )
    
    return {"message": "Menu item updated", "item": item}

@router.delete("/{restaurant_id}/{menu_id}")
def delete_menu_item(
    restaurant_id: int,
    menu_id: int,
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    menu_service.delete_menu_item(
        restaurant_id,
        menu_id
    )

    return {"message": "Menu item deleted"}
