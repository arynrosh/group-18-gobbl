from datetime import datetime
from typing import List, Any
from pathlib import Path
from app.schemas.notification import Notification
from app.repositories.notifications_repo import load_all_notifications, save_all_notifications

def _filter_notifications(field: str, value: Any) -> List[Notification]:
    """Returns notifications where the given field matches the value."""
    notifications = load_all_notifications()
    return [Notification(**n) for n in notifications if n[field] == value]

def send_notification(customer_id: str, order_id: str,  restaurant_id: int, message: str, override: Path = None) -> Notification:
    """
    Sends a notification to a customer and restaurant and saves it.

    Args:
        customer_id (str): ID of the customer to notify.
        restaurant_id (int): ID of the restaurant to notify.
        message (str): The notification message to send.
        override (Path, optional): A custom path to use instead of the default.

    Returns:
        Notification: The created notification object.
    """
    notifications = load_all_notifications(override)
    notification_id = len(notifications) + 1

    new_notification = {
        "notification_id": notification_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "restaurant_id": restaurant_id,
        "message": message,
        "status": "delivered",
        "timestamp": datetime.now().isoformat()
    }

    notifications.append(new_notification)
    save_all_notifications(notifications, override)

    return Notification(**new_notification)

def get_notifications_for_customer(customer_id: str, override: Path = None) -> List[Notification]:
    """
    Retrieves all notifications for a given customer.

    Args:
        customer_id (str): ID of the customer to retrieve notifications for.
        override (Path, optional): A custom path to use instead of the default.

    Returns:
        List[Notification]: A list of notifications for the customer.
    """
    notifications = load_all_notifications(override)
    return [Notification(**n) for n in notifications if n["customer_id"] == customer_id]

def get_notifications_for_restaurant(restaurant_id: int, override: Path = None) -> List[Notification]:
    """
    Retrieves all notifications for a given restaurant.

    Args:
        restaurant_id (int): ID of the restaurant to retrieve notifications for.
        override (Path, optional): A custom path to use instead of the default.

    Returns:
        List[Notification]: A list of notifications for the restaurant.
    """
    notifications = load_all_notifications(override)
    return [Notification(**n) for n in notifications if n["restaurant_id"] == restaurant_id]
