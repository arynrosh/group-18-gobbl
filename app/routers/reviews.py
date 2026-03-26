from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from app.auth.dependencies import require_roles
from app.schemas.review import ReviewCreate
from app.services import review_service

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_review(
    review_data: ReviewCreate,
    current_user: dict = Depends(require_roles("customer"))
):

    review = review_service.create_review(review_data)

    return {"message": "Review submitted successfully", "review": review}

@router.get("/order/{order_id}/items")
def get_review_items(order_id: str):
    items = review_service.get_reviewable_items_for_order(order_id)
    return {
        "order_id": order_id,
        "items": items
    }

@router.get("/restaurant/{restaurant_id}")
def get_reviews_for_restarant(restaurant_id: int):
    return review_service.list_reviews_for_restaurant(restaurant_id)

@router.get("/restaurant/{restaurant_id}/average")
def get_average_rating_for_restaurant(restaurant_id: int):
    avg_rating = review_service.get_average_rating_for_restaurant(restaurant_id)
    
    return {"average_rating": avg_rating}