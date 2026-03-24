from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    """
    Represents a signle item in an order.

    Attributes:
    - food_item (str) : name of the food item
    - quantity (int): quantity ordered
    - order_value (float): price per item
    - resturant_id (int): resturant it belongs to
    """
    food_item: str
    quantity: int = Field(..., gt = 0)
    order_value: float = Field(..., gt = 0)
    resturant_id: int = Field(..., gt = 0)

class Order(BaseModel):
    """
    Represents a customer order. 

    Attributes:
    -  order_id (str): Unique identifier for the order
    -  customer_id (str): ID of the customer placing the order
    -  restaurant_id (int): ID of the restaurant being ordered from
    -  items (List[OrderItem]): List of items in the order
    -  sent (bool): has the order been sent or not
    """

    order_id: str
    customer_id: str
    restaurant_id: int
    driver_distance: int
    assigned_driver_id: int
    items: List[OrderItem]
    sent: bool


class CostBreakdown(BaseModel): 
    """
    Represents the cost breakdown of an order.

    Attributes:
        order_id (str): The order this breakdown belongs to
        subtotal (float): Sum of all item costs
        tax (float): Tax applied to subtotal
        delivery_fee (float): Flat delivery fee
        total (float): Final total cost.
    """
    order_id: str
    subtotal: float
    tax: float
    delivery_fee: float
    total: float

class Status(BaseModel):
    """
    Used for communicating status of an order

    Attributes:
        order_id (str): The order that it is connected to
        current (str): The current status of the order
        complete (bool): Is the order complete or not
    """
    order_id: str
    current: str
    complete: bool
