import csv
from fastapi import Depends, HTTPException, status
from typing import Dict, Any, List, Optional

menu_db: Dict[int, Dict[str, Any]] = {}
menu_id_counter: int = 1

with open("app/data/food_delivery.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        item_id = int(row["item_id"])
        menu_db[item_id] = {
            "id": item_id,
            "name": row["name"],
            "price": float(row["price"]),
            "category": row["category"],
            "available": row["available"].lower() == "true",
            "restaurant_id": int(row["restaurant_id"])
        }

        menu_id_counter = max(menu_id_counter, item_id + 1)

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
    
def list_menu_items(
        restaurant_id: int,
        available: Optional[bool],
        category: Optional[str]
):
    
    items = [
        item for item in menu_db.values()
        if item.get("restaurant_id") == restaurant_id
    ]

    if available is not None:
        items = [
            item for item in items
            if item.get("available") == available
        ]

    if category is not None:
        items = [
            item for item in items
            if item.get("category", "").lower() == category.lower()
        ]

    return items

def create_menu_item(restaurant_id, item_data):
    global menu_id_counter
    new_item = {
        "id": menu_id_counter,
        "name": item_data.name,
        "price": item_data.price,
        "category": item_data.category,
        "available": item_data.available,
        "restaurant_id": restaurant_id
    }

    menu_db[menu_id_counter] = new_item
    menu_id_counter += 1

    return new_item

def update_menu_item(restaurant_id, menu_id, item_data):
    item = get_menu_item(menu_id)
    validate_item_belongs_to_restaurant(item, restaurant_id)

    if item_data.name is not None:
        item["name"] = item_data.name
    if item_data.price is not None:
        item["price"] = item_data.price
    if item_data.category is not None:
        item["category"] = item_data.category
    if item_data.available is not None:
        item["available"] = item_data.available
    
    return item

def delete_menu_item(restaurant_id, menu_id):
    
    item = get_menu_item(menu_id)
    validate_item_belongs_to_restaurant(item, restaurant_id)

    del menu_db[menu_id]
    