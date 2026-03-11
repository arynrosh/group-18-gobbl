from typing import List
from app.schemas.menu_item import MenuItem
import csv


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
    results = []
    for item in menu_items:
        if name.lower() in item["name"].lower():
            results.append(MenuItem(**item))
    return results


def search_by_price_range(min_price: float, max_price: float) -> List[MenuItem]:
    results = []
    for item in menu_items:
        if min_price <= item["price"] <= max_price:
            results.append(MenuItem(**item))
    return results