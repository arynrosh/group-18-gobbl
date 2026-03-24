from fastapi import FastAPI, status, HTTPException
from app.schemas.order import OrderItem, Order, Status
from app.services.menu_service import get_menu_item
from typing import Dict, Any
from app.schemas.menu_item import MenuItem
from app.repositories.order_repo import load_all_orders, save_all_orders, save_all_orderitems, load_all_orderitems, load_all_status

App = FastAPI()
menu_db: Dict[int, Dict[str, Any]] = {}
menu_id_counter: int = 1
#Task 4.1: Design database tables for Orders, Order Items, and Status Tracking
#Task 4.2: Implement API to create, modify, and submit orders (cart system)
#Task 4.3: Implement logic to prevent modifications after order completion
#Task 4.4: Implement API to fetch order status for a customer or restaurant
#Task 4.5: Unit tests for order creation, modification, and status updates-

"""def getItemFromMenu(item_id: int) -> MenuItem:
    item = menu_db.get(int)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with id {item_id} not found"
        )
    return item"""

def menuToOrderItem(item_id: int, quant: int, customer_id: str) -> MenuItem:
    food = get_menu_item(item_id)
    orderItem = orderItem(food_item = food.name,
                          quantity = quant,
                          order_value = food.price * quant,
                          resturant_id = food.resturant_id
    )
    currentOrder = getOrderId(customer_id)
    addToOrder(currentOrder, orderItem)


def addToOrder(order: Order, orderItem: OrderItem) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if order.sent == False:
        order.items.append(orderItem)
    return order

def removeFromOrder(order: Order, orderItem: OrderItem) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if order.sent == False:
            if orderItem in order.items:
                order.items.remove(orderItem)
    return order        

def sendOrder(order: Order) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    order.sent = True

def getOrderId(order: Order) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return order.order_id

def getOrderCustomer(order: Order) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return order.customer_id

def getOrderResturant(order: Order) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return order.restaurant_id

def getOrderItems(order: Order) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return order.items

def getOrderItem(food: OrderItem) -> OrderItem:
    ordered = load_all_orderitems()
    if food not in ordered: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    food_dict = [food.food_item, food.quantity, food.order_value, food.resturant_id]
    return food_dict

def getOrderSent(order: Order) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return order.sent

def getOrder(order: Order) -> Order:
    orders = load_all_orders()
    if order not in orders: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    Order_dict = [order.order_id, order.customer_id, order.restaurant_id, order.items, order.sent]
    return Order_dict

def updateStatus(status: Status, msg: str) -> Status:
    statuses = load_all_status()
    if status not in statuses:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if status.complete == False:
        status.current = msg

def completeOrderStatus(status: Status) -> Status:
    statuses = load_all_status()
    if status not in statuses:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    status.complete = True

def getStatusCurrent(status: Status) -> Status:
    statuses = load_all_status()
    if status not in statuses:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return status.current

def getStatusComplete(status: Status) -> Status:
    statuses = load_all_status()
    if status not in statuses:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return status.complete

