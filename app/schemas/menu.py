from pydantic import BaseModel, Field
from typing import Optional


class MenuItemCreate(BaseModel):
    food_item: str = Field(..., min_length=1, max_length=100)
    order_value: float = Field(..., gt=0)

class MenuItemUpdate(BaseModel):
    food_item: Optional[str] = Field(None, min_length=1, max_length=100)
    order_value: Optional[float] = Field(None, gt=0)

