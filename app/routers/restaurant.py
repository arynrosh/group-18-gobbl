from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, List, Any
from app.auth.dependencies import require_roles

router = APIRouter(prefix="/menu", tags=["menu"])

class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)

class MenuItemUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    price: float = Field(None, gt=0)

# In-memory menu storage  (idk what DB looks like yet)
menu_db: Dict[int, Dict[str, Any]] = {}
menu_id_counter: int = 1

def _get_menu_item(item_id: int) -> Dict[str, Any]:
    item = menu_db.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with id {item_id} not found"
            )
    return item

def _validate_item_belongs_to_restaurant(item: Dict[str, Any], restaurant_id: int):
# Checks if the menu item belongs to the specified restaurant
    if item.get("restaurant_id") != restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Menu item does not belong to this restaurant"
        )

@router.get("/{restaurant_id}", response_model=List[Dict[str, Any]])
# Returns all menu items for a given restaurant
def list_menu_items(restaurant_id: int):
    return [item for item in menu_db.values() if item.get("restaurant_id") == restaurant_id]


# CREATE menu item for restaurant (restaurant owner only)
@router.post("/{restaurant_id}",
             status_code=status.HTTP_201_CREATED,
             response_model=Dict[str, Any],
)
def create_menu_item(
    restaurant_id: int,
    item_data: MenuItemCreate,
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    global menu_id_counter
    new_item = {
        "id": menu_id_counter,
        "name": item_data.name,
        "price": item_data.price,
        "restaurant_id": restaurant_id
    }
    menu_db[menu_id_counter] = new_item
    menu_id_counter += 1

    return {"message": "Menu item created", "item": new_item}
    
# UPDATE menu item (restaurant owner only)
@router.put("/{restaurant_id}/{menu_id}", 
            response_model=Dict[str, Any]
)
def update_menu_item(
    restaurant_id: int,
    menu_id: int,
    item_data: MenuItemUpdate,
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    item = _get_menu_item(menu_id)
    _validate_item_belongs_to_restaurant(item, restaurant_id)

    if item_data.name is not None:
        item["name"] = item_data.name
    if item_data.price is not None:
        item["price"] = item_data.price

    return {"message": "Menu item updated", "item": item}

# DELETE menu item (restaurant owner only)
@router.delete("/{restaurant_id}/{menu_id}", 
               response_model=Dict[str, Any],
)
def delete_menu_item(
    restaurant_id: int,
    menu_id: int,
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    item = _get_menu_item(menu_id)
    _validate_item_belongs_to_restaurant(item, restaurant_id)

    del menu_db[menu_id]
    return {"message": "Menu item deleted"}