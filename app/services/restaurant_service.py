
from typing import List
from app.schemas.restaurant import Restaurant 


#hardcoded  temporary restaurant database
restaurants_db = {
    1: {"id": 1, "name": "Mucho Burrito", "cuisine": "Mexican", "location": "City_1"},
    2: {"id": 2, "name": "Fat Burger", "cuisine": "American", "location": "City_2"},
    3: {"id": 3, "name": "Noodle Box", "cuisine": "Asian", "location": "City_3"},
    4: {"id": 4, "name": "Cava", "cuisine": "Mediterranean", "location": "City_4"},
}

def search_by_name(name:str) -> List[Restaurant]:
    """
    Searches restaurants by name.

    Args:
        name (str): The name type to search for.

    Returns:
        List[Restaurant]: Matching restaurants.
    """
    results = []
    for restaurant in restaurants_db.values(): #loop through all values
        if name.lower() in restaurant["name"].lower():
            #add matching restaurants to results list
            results.append(Restaurant(**restaurant))
    return results 

def search_by_cuisine(cuisine: str) -> List[Restaurant]:
    """
    Searches restaurants by cuisine type.

    Args:
        cuisine (str): The cuisine type to search for.

    Returns:
        List[Restaurant]: Matching restaurants.
    """
    results = []
    for restaurant in restaurants_db.values():
        if cuisine.lower() in restaurant["cuisine"].lower():
            results.append(Restaurant(**restaurant))
    return results


