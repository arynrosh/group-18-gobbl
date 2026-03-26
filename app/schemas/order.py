from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    """
    Represents a signle item in an order.

    Attributes:
    - food_item (str) : name of the food item
    - quantity (int): quantity ordered
    -order_value (float): price per item
    """

    menu_item_id: int
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