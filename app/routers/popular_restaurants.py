from fastapi import APIRouter, Query
from app.services.popular_restaurants_service import ( get_popular_restaurants_by_orders, get_popular_restaurants_by_rating)

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/popular-restaurants/orders")
def popular_by_orders(limit: int = Query(default=10, ge=1)):
    """
    Returns the most popular restaurants based on number of orders.
    """
    return get_popular_restaurants_by_orders(limit)
@router.get("/popular-restaurants/ratings")
def popular_by_ratings(limit: int = Query(default=10, ge=1)):
    """
    Returns the most popular restaurants based on average rating.
    """
    return get_popular_restaurants_by_rating(limit)