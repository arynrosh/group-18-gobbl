from pydantic import BaseModel
class menu_schemas(BaseModel):
    menu_id: str #primary key
    restaurant_id:int #foreign key -> Restaurant.restaurant_id
    title: str
    is_active: bool = True
    