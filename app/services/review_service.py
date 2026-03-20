import json
from fastapi import HTTPException, status
from typing import Dict, Any, List

from app.schemas.review import ReviewCreate
from app.repositories.reviews_repo import (
    load_all_reviews,
    save_all_reviews,
    get_next_review_id,
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

def create_review(review_data: ReviewCreate, restaurant_id: int, customer_id: str) -> Dict[str, Any]:
    reviews = load_all_reviews()
    new_review = {
        "review_id": get_next_review_id(reviews),
        "order_id": review_data.order_id,
        "restaurant_id": restaurant_id,
        "customer_id": customer_id,
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