from pydantic import BaseModel

class Notification(BaseModel):
    
    notification_id: int
    customer_id: str
    restaurant_id: int
    message: str
    
    status: str
    timestamp: str

class NotificationRequest(BaseModel):
    
    customer_id: str
    restaurant_id: int
    message: str
class OrderPlacedRequest(BaseModel):
   
    order_id: str
    customer_id: str
    restaurant_id: int

class OutForDeliveryRequest(BaseModel):
   
    order_id: str
    customer_id: str
    restaurant_id: int
    driver_name: str

class OrderDeliveredRequest(BaseModel):
    
    order_id: str
    customer_id: str
    restaurant_id: int

class OrderDelayedRequest(BaseModel):
    
    order_id: str
    customer_id: str
    restaurant_id: int
    delay_minutes: float