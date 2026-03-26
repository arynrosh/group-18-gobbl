from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

class ItemRatingInput(BaseModel):
    menu_item_id: int = Field(..., example=1)
    food_item: str = Field(..., example="Burger")
    customer_rating: int = Field(..., ge=1, le=5, example=1)

#defined but not used
class Review(BaseModel):
    review_id: int
    order_id: str
    restaurant_id: int
    customer_id: int
    food_temperature: str
    food_freshness: int
    packaging_quality: int
    food_condition: str
    item_ratings: List[ItemRatingInput]

class ReviewCreate(BaseModel):
    order_id: str = Field(..., min_length=1, max_length=100)
    food_temperature: str = Field(..., min_length=1, max_length=100)
    food_freshness: int = Field(..., ge=1, le=5)
    packaging_quality: int = Field(..., ge=1, le=5)
    food_condition: str = Field(..., min_length=1, max_length=100)
    item_ratings: List[ItemRatingInput]