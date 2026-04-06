from typing import List
from app.repositories.order_repo import load_all_orders
from app.repositories.menu_repo import load_all_menu_items
from app.schemas.recommendation import RecommendedItem

def get_recommendations(customer_id: str, limit: int = 5) -> List[RecommendedItem]:
    
    orders = load_all_orders()
    menu_items = load_all_menu_items()

   
    customer_orders = [o for o in orders if o["customer_id"] == customer_id]

   
    if not customer_orders:
        return []

    
    ordered_cuisines = set()
    ordered_food_items = set()

    for order in customer_orders:
        for item in order.get("items", []):
            food_item = item.get("food_item")
            if food_item:
                ordered_food_items.add(food_item.lower())
            
            menu_match = next(
                (m for m in menu_items if m["food_item"] == food_item), None
            )
            if menu_match:
                ordered_cuisines.add(menu_match["cuisine"])

    if not ordered_cuisines:
        return []

   
    candidates = [
        item for item in menu_items
        if item["cuisine"] in ordered_cuisines
        and item["food_item"].lower() not in ordered_food_items
    ]

    
    candidates.sort(
        key=lambda x: x.get("customer_rating") or 0,
        reverse=True
    )

    
    return [
        RecommendedItem(
            menu_item_id=item["menu_item_id"],
            food_item=item["food_item"],
            cuisine=item["cuisine"],
            restaurant_name=item["restaurant_name"],
            order_value=item["order_value"],
            customer_rating=item.get("customer_rating")
        )
        for item in candidates[:limit]
    ]