from fastapi import FastAPI
from app.schemas.order import OrderItem, Order, Status
from app.services.menu_service import get_menu_item
from typing import Dict, Any
from app.schemas.menu_item import MenuItem
#add connection to menu_service to get items from menu

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
    if order.sent == False:
        order.items.append(orderItem)
    return order

def removeFromOrder(order: Order, orderItem: OrderItem) -> Order:
    if order.sent == False:
            if orderItem in order.items:
                order.items.remove(orderItem)
    return order        

def sendOrder(order: Order) -> Order:
    order.sent = True

def getOrderId(order: Order) -> Order:
    return order.order_id

def getOrderCustomer(order: Order) -> Order:
    return order.customer_id

def getOrderResturant(order: Order) -> Order:
    return order.restaurant_id

def getOrderItems(order: Order) -> Order:
    return order.items

def getOrderItem(food: OrderItem) -> OrderItem:
    return food

def getOrderSent(order: Order) -> Order:
    return order.sent

def getOrder(order: Order) -> Order:
    Order_dict = [order.order_id, order.customer_id, order.restaurant_id, order.items, order.sent]
    return Order_dict

def updateStatus(status: Status, msg: str) -> Status:
    if status.complete == False:
        status.current = msg

def completeOrderStatus(status: Status) -> Status:
    status.complete = True

def getStatusCurrent(status: Status) -> Status:
    return status.current

def getStatusComplete(status: Status) -> Status:
    return status.complete
