import requests
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from app.schemas.order import OrderItem, Order, Status

App = FastAPI()

#Task 4.1: Design database tables for Orders, Order Items, and Status Tracking
#Task 4.2: Implement API to create, modify, and submit orders (cart system)
#Task 4.3: Implement logic to prevent modifications after order completion
#Task 4.4: Implement API to fetch order status for a customer or restaurant
#Task 4.5: Unit tests for order creation, modification, and status updates-

def addToOrder(order: Order, orderItem: OrderItem) -> Order:
    if order.sent == False:
        order.items.append(orderItem)

def removeFromOrder(order: Order, orderItem: OrderItem) -> Order:
    if order.sent == False:
            if any(order.items, orderItem):
                order.items.remove(orderItem)

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

def getOrderSent(order: Order) -> Order:
    return order.sent

def updateStatus(status: Status, msg: str) -> Status:
    if status.complete == False:
        status.current = msg

def completeOrderStatus(status: Status) -> Status:
    status.complete = True

def getStatusCurrent(status: Status) -> Status:
    return status.current

def getStatusComplete(status: Status) -> Status:
    return status.complete
