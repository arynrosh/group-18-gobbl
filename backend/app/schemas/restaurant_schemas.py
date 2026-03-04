from pydantic import BaseModel
class Restaurant(BaseModel):
    restaurant_id: int #primary key
    location:str
    is_active: bool = True


    