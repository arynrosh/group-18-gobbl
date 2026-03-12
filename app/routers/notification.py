from fastapi import APIRouter
from typing import List
from app.services.notification_service import send_notification, get_notifications_for_customer, get_notifications_for_restaurant
from app.schemas.notification import Notification, NotificationRequest

router = APIRouter(prefix="/notifications", tags=["notifications"])



@router.post("/send", response_model=Notification)
def send_notification_endpoint(request: NotificationRequest):
    """
    Sends a notification to a customer and restaurant.
    """
    return send_notification(request.customer_id, request.restaurant_id, request.message)

@router.get("/customer/{customer_id}", response_model=List[Notification])
def get_customer_notifications(customer_id: str):
    """
    Retrieves all notifications for a given customer.
    """
    return get_notifications_for_customer(customer_id)

@router.get("/restaurant/{restaurant_id}", response_model=List[Notification])
def get_restaurant_notifications(restaurant_id: int):
    """
    Retrieves all notifications for a given restaurant.
    """
    return get_notifications_for_restaurant(restaurant_id)