from fastapi import APIRouter
from app.services.restaurant_service import search_by_name, search_by_cuisine
from app.schemas.restaurant import Restaurant
from typing import List

router = APIRouter(prefix = "/restaurant", tags=["restaurant"])

@router.get("/search/name", response_model = List[Restaurant])
def search_restaurants_by_name(name:str):
   #searches restaurant by name
    
    return search_by_name(name)
    

@router.get("/search/cuisine", response_model=List[Restaurant])
def search_restaurants_by_cuisine(cuisine: str):
    
   # Searches restaurants by cuisine type.

    
    
    return search_by_cuisine(cuisine)
            