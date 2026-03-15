import json
from fastapi import HTTPException, status
from typing import Dict, Any, List, Optional

menu_db: Dict[int, Dict[str, Any]] = {}
menu_id_counter: int = 1

def reset_menu_data():
    global menu_id_counter
    menu_db.clear()
    menu_id_counter = 1

    with open("app/data/menu.json", mode="r", encoding="utf-8") as file:
        items = json.load(file)
        for item in items:
            menu_db[item["id"]] = item
            menu_id_counter = max(menu_id_counter, item["id"] + 1)

def get_menu_item(item_id: int) -> Dict[str, Any]:
    item = menu_db.get(item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with id {item_id} not found"
        )
    return item

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

def list_menu_items(
        restaurant_id: int,
        price_tier: Optional[str] = None,
        min_rating: Optional[float] = None,
):
    
    items = [
        item for item in menu_db.values()
        if item.get("restaurant_id") == restaurant_id
    ]

    if price_tier is not None:
        items = [
            item for item in items
            if get_price_tier(item.get("order_value", 0)) == price_tier
        ]

    if min_rating is not None:
        items = [
            item for item in items
            if item.get("customer_rating") is not None 
            and item.get("customer_rating") >= min_rating
        ]
    
    return items

def create_menu_item(restaurant_id, item_data):
    global menu_id_counter
    new_item = {
        "id": menu_id_counter,
        "food_item": item_data.food_item,
        "order_value": item_data.order_value,
        "restaurant_id": restaurant_id
    }

    menu_db[menu_id_counter] = new_item
    menu_id_counter += 1

    return new_item

def update_menu_item(restaurant_id, menu_id, item_data):
    item = get_menu_item(menu_id)
    validate_item_belongs_to_restaurant(item, restaurant_id)

    if item_data.food_item is not None:
        item["food_item"] = item_data.food_item
    if item_data.order_value is not None:
        item["order_value"] = item_data.order_value
    
    return item

def delete_menu_item(restaurant_id, menu_id):
    
    item = get_menu_item(menu_id)
    validate_item_belongs_to_restaurant(item, restaurant_id)

    del menu_db[menu_id]
    