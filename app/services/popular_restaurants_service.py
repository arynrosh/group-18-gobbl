from typing import List, Dict, Any
from app.repositories.order_repo import load_all_orders
from app.repositories.reviews_repo import load_all_reviews

def _format_top_restaurants(
    restaurant_data: Dict[str, float],
    value_key: str,
    limit: int
) -> List[Dict[str, Any]]:
    sorted_restaurants = sorted(
        restaurant_data.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"restaurant_id": rid, value_key: value}
        for rid, value in sorted_restaurants[:limit]
    ]
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

    return _format_top_restaurants(order_counts, "total_orders", limit)

    
def get_popular_restaurants_by_rating(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Returns the most popular restaurants based on average rating.
    """
    reviews = load_all_reviews()

    if not reviews:
        return []

    restaurant_ratings = {}

    for review in reviews:
        try:
            restaurant_id = review["restaurant_id"]
            rating = float(review["rating"])
            if restaurant_id not in restaurant_ratings:
                restaurant_ratings[restaurant_id] = []
            restaurant_ratings[restaurant_id].append(rating)
        except (KeyError, ValueError):
            continue

    averages = {
        rid: round(sum(ratings) / len(ratings), 2)
        for rid, ratings in restaurant_ratings.items()
    }

    return _format_top_restaurants(averages, "average_rating", limit)