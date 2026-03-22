from typing import List, Dict, Any
from app.repositories.statistics_repo import load_all_orders
from app.repositories.reviews_repo import load_all_reviews


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

    sorted_restaurants = sorted(
        averages.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"restaurant_id": rid, "average_rating": avg}
        for rid, avg in sorted_restaurants[:limit]
    ]