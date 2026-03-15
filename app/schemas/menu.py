from pydantic import BaseModel, Field
from typing import Optional


class MenuItemCreate(BaseModel):
    food_item: str = Field(..., min_length=1, max_length=100)
    order_value: float = Field(..., gt=0)

class MenuItemUpdate(BaseModel):
    food_item: Optional[str] = Field(None, min_length=1, max_length=100)
    order_value: Optional[float] = Field(None, gt=0)

#andrea, you need to move this to another schemas file, since it's not related to menu item
class Restaurant(BaseModel):

    id: int
    name: str
    cuisine: str
    location: str