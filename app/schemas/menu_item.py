from pydantic import BaseModel

class MenuItem(BaseModel):
    """
    represents a menu item.

    Attributes: 
    id (int): unique identifier
    name (string): menu item name
    price (float): menu item price
    restaurant_id (int): ID of the restaurant this item belongs to
    """

    id: int
    name: str
    price: float
    restaurant_id: int
    

