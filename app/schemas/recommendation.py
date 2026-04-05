from pydantic import BaseModel

class RecommendedItem(BaseModel):
    menu_item_id: int
    food_item: str
    cuisine: str
    restaurant_id: int
    restaurant_name: str
    order_value: float
    customer_rating: float = None