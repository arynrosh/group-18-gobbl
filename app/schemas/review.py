from pydantic import BaseModel, Field
from typing import Optional

class Review(BaseModel):
    review_id: int
    order_id: int
    restaurant_id: int
    customer_id: int
    rating: int
    food_temperature: str
    food_freshness: int
    packaging_quality: int
    food_condition: str

class ReviewCreate(BaseModel):
    order_id: int = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)
    food_temperature: str = Field(..., min_length=1, max_length=100)
    food_freshness: int = Field(..., ge=1, le=5)
    packaging_quality: int = Field(..., ge=1, le=5)
    food_condition: str = Field(..., min_length=1, max_length=100)

class ReviewResponse(BaseModel):
    review_id: int
    order_id: int
    restaurant_id: int
    customer_id: int
    rating: int
    food_temperature: str
    food_freshness: int
    packaging_quality: int
    food_condition: str
