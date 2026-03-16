import csv
from typing import List
from app.schemas.menu_item import MenuItem

menu_items = []

with open("data/food_delivery.csv", newline="") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        menu_items.append({
            "id": i,
            "name": row["food_item"],
            "price": float(row["order_value"]),
            "restaurant_id": int(row["restaurant_id"])
        })

def search_by_name(name: str) -> List[MenuItem]:
   #searhes menu item by name across all restaurants
    results = []
    for item in menu_items:
        if name.lower() in item["name"].lower():
            results.append(MenuItem(**item))
    return results
