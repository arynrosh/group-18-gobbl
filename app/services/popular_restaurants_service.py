from typing import List, Dict, Any
from app.repositories.statistics_repo import load_all_orders

def get_popular_restaurants_by_orders(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Returns the most popular restaurants based on number of orders.
    """
    orders = load_all_orders()

    if not orders:
        return []

    order_counts = {}

    for order in orders:
        try:
            restaurant_id = order["restaurant_id"]
            if restaurant_id not in order_counts:
                order_counts[restaurant_id] = 0
            order_counts[restaurant_id] += 1
        except KeyError:
            continue

    sorted_restaurants = sorted(
        order_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"restaurant_id": rid, "total_orders": count}
        for rid, count in sorted_restaurants[:limit]
    ]