from pydantic import BaseModel

class MenuItem(BaseModel):
    menu_item_id: int
    food_item: str
    order_value: float
    restaurant_id: int
    restaurant_name: str
    cuisine: str
