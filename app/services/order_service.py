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

def addToOrder(orderItem: OrderItem) -> Order:
    if Order.sent == False:
        Order.items.append(orderItem)

def removeFromOrder(orderItem: OrderItem) -> Order:
    if Order.sent == False:
            if any(Order.items, orderItem):
                Order.items.remove(orderItem)

def sendOrder(orderId: str) -> Order:
    Order.sent = True

def updateStatus(status: str) -> Status:
    if Status.complete == False:
        current = status

def completeOrderStatus() -> Status:
    Status.complete = True


