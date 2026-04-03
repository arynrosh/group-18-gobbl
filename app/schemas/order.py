from pydantic import BaseModel, Field
from typing import List, Optional

class OrderItem(BaseModel):
    food_item: str
    quantity: int = Field(..., gt = 0)
    order_value: float = Field(..., gt = 0)

class Order(BaseModel):
    order_id: str
    customer_id: str
    restaurant_id: int
    delivery_distance: float
    delivery_time: float = None  # in minutes, optional
    assigned_driver_id: int
    items: List[OrderItem]
    sent: bool
    diet_restrictions: Optional[List[str]] = None

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