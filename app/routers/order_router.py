from fastapi import APIRouter, Depends
from app.services.order_service import addToOrder, removeFromOrder, sendOrder, getOrder, getOrderItem
from app.schemas.Order import Order, OrderItem
from app.schemas.restaurant import Restaurant
from app.auth.dependencies import get_current_user
    
# Reference:
# router = APIRouter(prefix="/menu", tags=["menu"])
OrdeRouter = APIRouter(prefix="/orders", tags=["order"])
foodRouter = APIRouter(prefix="/OrderItem", tags=["food_item"])

@OrdeRouter.post("/{order_id}/")
def createOrder(order_id: str, resturant_id: int, current_user: dict = Depends(get_current_user)):
    return Order(order_id = order_id,
        customer_id = current_user,
        restaurant_id = resturant_id,
        items = [],
        sent = False)

@OrdeRouter.get("/{order_id}/")
def getOrder(order_id: str):
    return getOrder(order_id)

@OrdeRouter.put("/{order_id}/")
def updateOrderAdd(order_id: str, food: str):
    return addToOrder(order_id, food)

@OrdeRouter.put("/{order_id}/")
def updateOrderRemove(order_id: str, food: str):
    return removeFromOrder(order_id, food)

@OrdeRouter.put("/{order_id}/")
def updateOrderSend(order_id: str):
    return sendOrder(order_id)

@foodRouter.get("/{food_item}/")
def getFood(food_item: str):
    return getOrderItem(food_item)

@foodRouter.post("/{food_item}/")
def createOrderItem(food_name: str, howMany: int, cost: float, resturant: int):
    return OrderItem(food_item = food_name,
    quantity = howMany,
    order_value = cost,
    resturant_id = resturant)

