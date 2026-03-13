from datetime import datetime
from typing import List
from app.schemas.notification import Notification
from app.repositories.notifications_repo import load_all_notifications, save_all_notifications

def send_notification(customer_id: str, restaurant_id: int, message: str) -> Notification:
    """
    Sends a notification to a customer and restaurant and saves it.
    """
    notifications = load_all_notifications()
    notification_id = len(notifications) + 1
    
    new_notification = {
        "notification_id": notification_id,
        "customer_id": customer_id,
        "restaurant_id": restaurant_id,
        "message": message,
        "status": "delivered",
        "timestamp": datetime.now().isoformat()
    }
    
    notifications.append(new_notification)
    save_all_notifications(notifications)
    
    return Notification(**new_notification)

def get_notifications_for_customer(customer_id: str) -> List[Notification]:
    """
    Retrieves all notifications for a given customer.
    """
    notifications = load_all_notifications()
    return [Notification(**n) for n in notifications if n["customer_id"] == customer_id]

def get_notifications_for_restaurant(restaurant_id: int) -> List[Notification]:
    """
    Retrieves all notifications for a given restaurant.
    """
    notifications = load_all_notifications()
    return [Notification(**n) for n in notifications if n["restaurant_id"] == restaurant_id]