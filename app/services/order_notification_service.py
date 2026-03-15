from app.services.notification_service import send_notification
from app.schemas.notification import Notification

def notify_order_placed(order_id: str, customer_id: str, restaurant_id: int) -> Notification:
    message = f"Your order {order_id} has been placed successfully."
    return send_notification(customer_id, restaurant_id, message)

def notify_out_for_delivery(order_id: str, customer_id: str, restaurant_id: int, driver_name: str) -> Notification:
    message = f"Your order {order_id} is out for delivery with driver {driver_name}."
    return send_notification(customer_id, restaurant_id, message)

def notify_order_delivered(order_id: str, customer_id: str, restaurant_id: int) -> Notification:
    message = f"Your order {order_id} has been delivered. Enjoy your meal!"
    return send_notification(customer_id, restaurant_id, message)

def notify_order_delayed(order_id: str, customer_id: str, restaurant_id: int, delay_minutes: float) -> Notification:
    message = f"Your order {order_id} is delayed by {delay_minutes} minutes. We apologize for the inconvenience."
    return send_notification(customer_id, restaurant_id, message)