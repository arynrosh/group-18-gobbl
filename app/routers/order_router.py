from fastapi import APIRouter, Depends, status, HTTPException
from app.services.order_service import addToOrder, removeFromOrder, sendOrder, getOrder, getOrderItem, updateStatus, completeOrderStatus
from app.schemas.order import Order, OrderItem, Status
from app.auth.dependencies import require_roles
from app.repositories.order_repo import load_all_orders, save_all_orders, save_all_orderitems

#http://127.0.0.1:8000/docs#/menu/search_menu_items_by_name_menu_search_name_get    
OrdeRouter = APIRouter(prefix="/orders", tags=["order_id"])
foodRouter = APIRouter(prefix="/OrderItem", tags=["food_item"])
statusRouter = APIRouter(prefix="/status", tags=["order_id"])

@OrdeRouter.post("/orders/{order_id}/create_order/")
def createOrder(order_id: str, resturant_id: int, dis: int, driver: int, current_user: dict = Depends(require_roles("customer"))):
    return Order(order_id = order_id,
        customer_id = current_user,
        restaurant_id = resturant_id,
        driver_distance = dis,
        assigned_driver_id = driver,
        items = [],
        sent = False)

@OrdeRouter.get("/orders/{order_id}/")
def getOrder(order_id: str):
    return getOrder(order_id)

@OrdeRouter.put("/orders/{order_id}/")
def updateOrderAdd(order_id: str, food: str):
    return addToOrder(order_id, food)

@OrdeRouter.put("/orders/{order_id}/")
def updateOrderRemove(order_id: str, food: str):
    return removeFromOrder(order_id, food)

@OrdeRouter.put("/orders/{order_id}/")
def updateOrderSend(order_id: str):
    return sendOrder(order_id)

@foodRouter.get("/OrderItem/{food_item}/")
def getFood(food_item: str):
    return getOrderItem(food_item)

@foodRouter.post("/OrderItem/{food_item}/")
def createOrderItem(food_name: str, howMany: int, cost: float, resturant: int):
    return OrderItem(food_item = food_name,
    quantity = howMany,
    order_value = cost,
    resturant_id = resturant)

@statusRouter.post("/status/{order_id}/")
def createStatus(orderid: str):
    return Status(order_id= orderid,
                  current = "Sent",
                  complete = False)

@statusRouter.put("/status/{order_id}/")
def updateStatusRout(orderid: str, msg: str):
    return updateStatus(orderid, msg)

@statusRouter.put("/status/{order_id}/")
def completeStatusRout(orderid: str):
    return completeOrderStatus(orderid)