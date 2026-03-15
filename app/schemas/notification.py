from pydantic import BaseModel

class Notification(BaseModel):
    """
    Represents a notification sent to a customer or restaurant.
    """
    notification_id: int
    customer_id: str
    restaurant_id: int
    message: str
    # Indicates whether the notification has been delivered or is pending
    status: str
    timestamp: str

class NotificationRequest(BaseModel):
    """
    Request body for sending a notification.
    """
    customer_id: str
    restaurant_id: int
    message: str