from pydantic import BaseModel, Field
from typing import Optional

#defined but not used (yet)
class MenuItem(BaseModel):
    menu_item_id: int
    restaurant_id: int
    restaurant_name: str
    cuisine: str
    food_item: str
    order_value: float
    customer_rating: Optional[float] = None
    rating_count: Optional[int] = None
    delivery_time_actual: Optional[float] = None

class MenuItemCreate(BaseModel):
    restaurant_name: str = Field(..., min_length=1, max_length=100)
    cuisine: str = Field(..., min_length=1, max_length=100)
    food_item: str = Field(..., min_length=1, max_length=100)
    order_value: float = Field(..., gt=0)

class MenuItemUpdate(BaseModel):
    restaurant_name: Optional[str] = Field(None, min_length=1, max_length=100)
    cuisine: Optional[str] = Field(None, min_length=1, max_length=100)
    food_item: Optional[str] = Field(None, min_length=1, max_length=100)
    order_value: Optional[float] = Field(None, gt=0)