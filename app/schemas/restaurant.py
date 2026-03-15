from pydantic import BaseModel, Field
from typing import Optional


class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = Field(None, min_length=1, max_length=50)
    available: bool = True

class MenuItemUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    price: float = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    available: Optional[bool] = None

class Restaurant(BaseModel):

    id: int
    name: str
    cuisine: str
    location: str