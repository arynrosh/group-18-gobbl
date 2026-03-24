from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.notification_service import send_notification, get_notifications_for_customer, get_notifications_for_restaurant
from app.schemas.notification import Notification, NotificationRequest
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/notifications", tags=["notifications"])



@router.post("/send", response_model=Notification)
def send_notification_endpoint(request: NotificationRequest, current_user: dict = Depends(get_current_user)):
    """
    Sends a notification to a customer and restaurant.
    Accessible by admin Only.
    """
    if current_user.get("role") not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )
    return send_notification(request.customer_id, request.restaurant_id, request.message)

@router.get("/customer/{customer_id}", response_model=List[Notification])
def get_customer_notifications(customer_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieves all notifications for a given customer.
    Accessible by customer and admins only. 
    """
    if current_user.get("role") not in ["customer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Customers and admins only."
        )
    return get_notifications_for_customer(customer_id)

@router.get("/restaurant/{restaurant_id}", response_model=List[Notification])
def get_restaurant_notifications(restaurant_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retrieves all notifications for a given restaurant.
    Accessible by restaurant owners and admin only
    """
    if current_user.get("role") not in ["restaurant_owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Restaurant owners and admins only."
        )
    return get_notifications_for_restaurant(restaurant_id)