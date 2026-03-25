from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    restaurant_id: int = Field(..., gt=0)
    food_item: str
    quantity: int = Field(..., gt=0)
    order_value: float = Field(..., gt=0)

class Order(BaseModel):
    order_id: str
    customer_id: str
    delivery_distance: int
    assigned_driver_id: int | None = None
    items: List[OrderItem]
    sent: bool

class CostBreakdown(BaseModel):
    order_id: str
    subtotal: float
    tax: float
    delivery_fee: float
    total: float

class Status(BaseModel):
    order_id: str
    current: str
    complete: bool