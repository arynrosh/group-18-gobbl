from fastapi import HTTPException, status
from typing import Dict, Any, List, Optional

from app.schemas.menu import MenuItemCreate, MenuItemUpdate
from app.repositories.menu_repo import (
    load_all_menu_items,
    save_all_menu_items,
    get_next_menu_id,
)

def get_menu_item(food_item: str, restaurant_id: int) -> Dict[str, Any]:
    items = load_all_menu_items()

    for item in items:
        if item["food_item"] == food_item and item["restaurant_id"] == restaurant_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item {food_item} not found for restaurant {restaurant_id}"
    )

def validate_item_belongs_to_restaurant(item: Dict[str, Any], restaurant_id: int):
    if item.get("restaurant_id") != restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Menu item does not belong to this restaurant"
        )
    
def get_price_tier(price: float) -> str:
    if price < 15:
        return "$"
    elif price < 25:
        return "$$"
    elif price < 40:
        return "$$$"
    else:
        return "$$$$"

def list_menu_items(restaurant_id: int, price_tier: Optional[str] = None, min_rating: Optional[float] = None) -> List[Dict[str, Any]]:
    items = load_all_menu_items()
    filtered_items = [
        item for item in items
        if item.get("restaurant_id") == restaurant_id
    ]

    if price_tier is not None:
        filtered_items = [
            item for item in filtered_items
            if get_price_tier(item.get("order_value", 0)) == price_tier
        ]

    if min_rating is not None:
        filtered_items = [
            item for item in filtered_items
            if item.get("customer_rating") is not None 
            and item.get("customer_rating") >= min_rating
        ]
    
    return filtered_items

def create_menu_item(restaurant_id: int, item_data: MenuItemCreate) -> Dict[str, Any]:
    items = load_all_menu_items()

    new_item = {
        "menu_item_id": get_next_menu_id(items),
        "restaurant_id": restaurant_id,
        "restaurant_name": item_data.restaurant_name,
        "cuisine": item_data.cuisine,
        "food_item": item_data.food_item,
        "order_value": item_data.order_value,
        "restaurant_id": restaurant_id,
        "customer_rating": None,
        "delivery_time_actual": None
    }

    items.append(new_item)
    save_all_menu_items(items)

    return new_item

def update_menu_item(restaurant_id: int, menu_id: int, item_data: MenuItemUpdate) -> Dict[str, Any]:
    items = load_all_menu_items()

    for item in items:
        if item["menu_item_id"] == menu_id:
            validate_item_belongs_to_restaurant(item, restaurant_id)

            if item_data.restaurant_name is not None:
                item["restaurant_name"] = item_data.restaurant_name
            if item_data.cuisine is not None:
                item["cuisine"] = item_data.cuisine        
            if item_data.food_item is not None:
                item["food_item"] = item_data.food_item
            if item_data.order_value is not None:
                item["order_value"] = item_data.order_value

            save_all_menu_items(items)
            return item
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item with id {menu_id} not found"
    )

def delete_menu_item(restaurant_id: int, menu_id: int):
    items = load_all_menu_items()

    for delete_item, item in enumerate(items):
        if item["menu_item_id"] == menu_id:
            validate_item_belongs_to_restaurant(item, restaurant_id)
            del items[delete_item]
            save_all_menu_items(items)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item with id {menu_id} not found"
    )
    