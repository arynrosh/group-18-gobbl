import json
from pathlib import Path
from fastapi import HTTPException, status
from typing import Dict, Any, List

from app.schemas.order import Order
from app.schemas.review import ReviewCreate
from app.repositories.reviews_repo import (
    load_all_reviews,
    save_all_reviews,
    get_next_review_id,
)

ORDER_PATH = Path(__file__).resolve().parents[1] / "data" / "mock_data" / "orders_mock.json"

def load_all_orders() -> List[Dict[str, Any]]:
    if not ORDER_PATH.exists():
        return []
    
    with ORDER_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def get_order_or_404(order_id: str) -> Dict[str, Any]:
    orders = load_all_orders()
    for order in orders:
        if order["order_id"] == order_id:
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with id {order_id} not found"
    )

def get_review(review_id: int) -> Dict[str, Any]:
    reviews = load_all_reviews()

    for review in reviews:
        if review["review_id"] == review_id:
            return review
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Review with id {review_id} not found"
    )

def create_review(review_data: ReviewCreate) -> Dict[str, Any]:
    reviews = load_all_reviews()
    order = get_order_or_404(review_data.order_id)
    new_review = {
        "review_id": get_next_review_id(reviews),
        "order_id": review_data.order_id,
        "restaurant_id": order["restaurant_id"],
        "customer_id": order["customer_id"],
        "rating": review_data.rating,
        "food_temperature": review_data.food_temperature,
        "food_freshness": review_data.food_freshness,
        "packaging_quality": review_data.packaging_quality,
        "food_condition": review_data.food_condition
    }

    reviews.append(new_review)
    save_all_reviews(reviews)

    return new_review

def list_reviews_for_restaurant(restaurant_id: int) -> List[Dict[str, Any]]:
    reviews = load_all_reviews()

    return[
        review for review in reviews
        if review["restaurant_id"] == restaurant_id
    ]

def get_average_rating(restaurant_id: int) -> float:
    reviews = list_reviews_for_restaurant(restaurant_id)
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reviews found for this restaurant"
        )
    
    avg = sum(rating["rating"] for rating in reviews) / len(reviews)

    return round(avg, 2)