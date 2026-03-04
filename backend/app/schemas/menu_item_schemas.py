from pydantic import BaseModel
class menu_item(BaseModel):
    menu_item_id: str #primary key
    menu_id: str #foreign key -> Menu.menu_id
    name: str
    price: float
    category: str
    is_available: bool = True