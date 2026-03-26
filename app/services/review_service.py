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
from app.repositories.menu_repo import (
    load_all_menu_items,
    save_all_menu_items,
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

def get_reviewable_items_for_order(order_id: str) -> List[Dict[str, Any]]:
    order = get_order_or_404(order_id)

    items = order.get("items", [])
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found for this order"            
        )
    
    return [
        {
            "menu_item_id": item["menu_item_id"],
            "food_item": item["food_item"],
            "customer_rating": None           
        }
        for item in items
    ]

def get_review(review_id: int) -> Dict[str, Any]:
    reviews = load_all_reviews()

    for review in reviews:
        if review["review_id"] == review_id:
            return review
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Review with id {review_id} not found"
    )

def get_menu_item(menu_item_id: int) -> Dict[str, Any]:
    menu_items = load_all_menu_items()
    for item in menu_items:
        if item["menu_item_id"] == menu_item_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item with id {menu_item_id} not found"
    )

def recalculate_menu_item_ratings() -> None:
    reviews = load_all_reviews()
    menu_items = load_all_menu_items()

    for menu_item in menu_items:
        ratings = []

        for review in reviews:
            for item_rating in review.get("item_ratings", []):
                if (item_rating["menu_item_id"] == menu_item["menu_item_id"] and item_rating["customer_rating"] is not None):
                    ratings.append(item_rating["customer_rating"])

        if ratings:
            menu_item["customer_rating"] = round(sum(ratings) / len(ratings), 2)
            menu_item["rating_count"] = len(ratings)
        else:
            menu_item["customer_rating"] = None
            menu_item["rating_count"] = 0
    
    save_all_menu_items(menu_items)

def create_review(review_data: ReviewCreate) -> Dict[str, Any]:
    reviews = load_all_reviews()
    order = get_order_or_404(review_data.order_id)

    item_ratings = []
    order_item_ids = [order_item["menu_item_id"] for order_item in order.get("items", [])]

    for item in review_data.item_ratings:
        menu_item = get_menu_item(item.menu_item_id)
        if menu_item["restaurant_id"] != order["restaurant_id"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item {item.menu_item_id} does not match the restaurant for this order"
            )
        if item.menu_item_id not in order_item_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item {item.menu_item_id} was not part of order {order['order_id']}"
            )

        item_ratings.append({
            "menu_item_id": menu_item["menu_item_id"],
            "food_item": menu_item["food_item"],
            "customer_rating": item.customer_rating
        })

    new_review = {
        "review_id": get_next_review_id(reviews),
        "order_id": review_data.order_id,
        "restaurant_id": order["restaurant_id"],
        "customer_id": order["customer_id"],
        "food_temperature": review_data.food_temperature,
        "food_freshness": review_data.food_freshness,
        "packaging_quality": review_data.packaging_quality,
        "food_condition": review_data.food_condition,
        "item_ratings": item_ratings
    }

    reviews.append(new_review)
    save_all_reviews(reviews)
    recalculate_menu_item_ratings()

    return new_review

def list_reviews_for_restaurant(restaurant_id: int) -> List[Dict[str, Any]]:
    reviews = load_all_reviews()

    return[
        review for review in reviews
        if review["restaurant_id"] == restaurant_id
    ]

def get_average_rating_for_restaurant(restaurant_id: int) -> float:
    menu_items = load_all_menu_items()

    restaurant_items = [
        item for item in menu_items
        if item["restaurant_id"] == restaurant_id and item.get("customer_rating") is not None
    ]

    if not restaurant_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No rated menu items found for this restaurant"
        )
    
    avg = sum(item["customer_rating"] for item in restaurant_items) / len(restaurant_items)

    return round(avg, 2)