from fastapi import APIRouter
from app.services.restaurant_service import search_by_name, search_by_cuisine
from app.schemas.restaurant import Restaurant
from typing import List

router = APIRouter(prefix = "/restaurant", tags=["restaurant"])

@router.get("/search/name", response_model = List[Restaurant])
def search_restaurants_by_name(name:str):
   
    
    return search_by_name(name)
    """
    Searches restaurants by name type.

    Args:
        name (str): The cuisine type to search for.

    Returns:
        List[Restaurant]: Matching restaurants.
        """

@router.get("/search/cuisine", response_model=List[Restaurant])
def search_restaurants_by_cuisine(cuisine: str):
    """
    Searches restaurants by cuisine type.

    Args:
        cuisine (str): The cuisine type to search for.

    Returns:
        List[Restaurant]: Matching restaurants.
    """
    return search_by_cuisine(cuisine)
            