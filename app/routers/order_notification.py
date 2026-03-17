from fastapi import APIRouter
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

router = APIRouter(prefix="/order-notifications", tags=["order-notifications"])

@router.post("/placed", response_model=Notification)
def order_placed(request: OrderPlacedRequest):
    
    # Triggers a notification when an order is placed.

    return notify_order_placed(request.order_id, request.customer_id, request.restaurant_id)

@router.post("/out-for-delivery", response_model=Notification)
def out_for_delivery(request: OutForDeliveryRequest):
    
    #Triggers a notification when an order is out for delivery.
    
    return notify_out_for_delivery(request.order_id, request.customer_id, request.restaurant_id, request.driver_name)

@router.post("/delivered", response_model=Notification)
def order_delivered(request: OrderDeliveredRequest):
    
    #Triggers a notification when an order is delivered.
    
    return notify_order_delivered(request.order_id, request.customer_id, request.restaurant_id)

@router.post("/delayed", response_model=Notification)
def order_delayed(request: OrderDelayedRequest):
    
    #Triggers a notification when an order is delayed.
    
    return notify_order_delayed(request.order_id, request.customer_id, request.restaurant_id, request.delay_minutes)