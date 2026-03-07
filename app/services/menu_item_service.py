from typing import List
from app.schemas.menu_item import MenuItem
from app.routers.restaurant import menu_db

def search_by_name(name: str) -> List[MenuItem]:
    """
    Searches menu items by name across all restaurants.

    Args:
        name (str): The name to search for.

    Returns:
        List[MenuItem]: Matching menu items.
    """
    results = []
    for item in menu_db.values():
        if name.lower() in item["name"].lower():
            results.append(MenuItem(**item))
    return results


def search_by_price_range(min_price: float, max_price: float) -> List[MenuItem]:
    """
    Searches menu items within a price range across all restaurants.

    Args:
        min_price (float): Minimum price.
        max_price (float): Maximum price.

    Returns:
        List[MenuItem]: Matching menu items.
    """
    results = []
    for item in menu_db.values():
        if min_price <= item["price"] <= max_price:
            results.append(MenuItem(**item))
    return results