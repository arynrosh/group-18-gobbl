from pydantic import BaseModel
class Restaurant(BaseModel):
    """
     Represents a restaurant.

    Attributes:
        id (int): Unique identifier.
        name (str): Restaurant name.
        cuisine (str): Cuisine type.
        location (str): Restaurant location.
    """
    id:int
    name: str
    cuisine: str
    location: str
