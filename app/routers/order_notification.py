from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.notification import (
    Notification,
    OrderPlacedRequest,
    OutForDeliveryRequest,
    OrderDeliveredRequest,
    OrderDelayedRequest
)
from app.services.order_notification_service import (
    notify_order_placed,
    notify_out_for_delivery,
    notify_order_delivered,
    notify_order_delayed
)
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/order-notifications", tags=["order-notifications"])

@router.post("/placed", response_model=Notification)
def order_placed(request: OrderPlacedRequest, current_user: dict = Depends(get_current_user)):
    
    # Triggers a notification when an order is placed.
    #Accessible by admins only.
    if current_user.get("role") not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )

    return notify_order_placed(request.order_id, request.customer_id, request.restaurant_id)

@router.post("/out-for-delivery", response_model=Notification)
def out_for_delivery(request: OutForDeliveryRequest, current_user: dict = Depends(get_current_user)):
    
    #Triggers a notification when an order is out for delivery.Admin only.
    if current_user.get("role") not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )
    
    return notify_out_for_delivery(request.order_id, request.customer_id, request.restaurant_id, request.driver_name)

@router.post("/delivered", response_model=Notification)
def order_delivered(request: OrderDeliveredRequest, current_user: dict = Depends(get_current_user)):
    
    #Triggers a notification when an order is delivered.Admin only.
    if current_user.get("role") not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )
    
    return notify_order_delivered(request.order_id, request.customer_id, request.restaurant_id)

@router.post("/delayed", response_model=Notification)
def order_delayed(request: OrderDelayedRequest, current_user: dict = Depends(get_current_user)):
    
    #Triggers a notification when an order is delayed.Admin only
    if current_user.get("role") not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )
    
    return notify_order_delayed(request.order_id, request.customer_id, request.restaurant_id, request.delay_minutes)