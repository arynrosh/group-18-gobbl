from pydantic import BaseModel
from typing import Optional

class Order(BaseModel):
    order_id: str                # PRIMARY KEY
    customer_id: str             # FOREIGN KEY -> Users.user_id
    restaurant_id: int           # FOREIGN KEY -> Restaurants.restaurant_id
    status: str                  # NOT NULL, one of: PENDING, CONFIRMED, PREPARING, COMPLETED, CANCELLED
    total_price: float           # NOT NULL, must be >= 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class OrderItem(BaseModel):
    order_item_id: str           # PRIMARY KEY
    order_id: str                # FOREIGN KEY -> Orders.order_id
    menu_item_id: str            # FOREIGN KEY -> MenuItems.menu_item_id, UNIQUE per order
    quantity: int                # NOT NULL, must be > 0
    item_price: float            # NOT NULL, must be >= 0

class OrderStatusTracking(BaseModel):
    status_id: str               # PRIMARY KEY
    order_id: str                # FOREIGN KEY -> Orders.order_id
    status: str                  # NOT NULL, one of: PENDING, CONFIRMED, PREPARING, COMPLETED, CANCELLED
    updated_at: Optional[str] = None