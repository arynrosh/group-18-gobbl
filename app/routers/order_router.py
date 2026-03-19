from fastapi import APIRouter, Depends
from app.services.order_service import addToOrder, removeFromOrder, sendOrder, getOrder
from app.schemas.Order import Order
from app.schemas.restaurant import Restaurant
from app.auth.dependencies import get_current_user
    
# Reference:
# router = APIRouter(prefix="/menu", tags=["menu"])
router = APIRouter(prefix="/order", tags=["order"])

@router.post("/{order_id}/")
def createOrder(order_id: str, current_user: dict = Depends(get_current_user), resturant_id: int):
    return Order(order_id = order_id,
        customer_id = current_user,
        restaurant_id = resturant_id,
        items = [],
        sent = False)

@router.get("/{order_id}/")
def getOrder(order_id: str):
    return getOrder(order_id)

@router.put("/{order_id}/")
def updateOrderAdd(order_id: str, food: str):
    return addToOrder(order_id, food)

@router.put("/{order_id}/")
def updateOrderRemove(order_id: str, food: str):
    return removeFromOrder(order_id, food)

@router.put("/{order_id}/")
def updateOrderSend(order_id: str):
    return sendOrder(order_id)