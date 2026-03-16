import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.services.order_service import App
from app.schemas.order import Order, OrderItem, Status
#app\services\order_service.py
from app.services.order_service import updateStatus, completeOrderStatus, addToOrder, removeFromOrder, sendOrder

client2 = TestClient(App)

def statusTester():
    return Status("1d8e87M")

def orderItemTester():
    foodName = "Tacos"
    foodPrice = 12.99
    foodRid = 13
    return OrderItem(foodName, foodPrice, foodRid)

def orderTester():
    return Order("2f9r98Z", "custest")


def test_updateStatus(statusTester):
    statusUpdate = "Ready"
    statusTester.updateStatus("Ready")
    result = statusTester.current
    assert statusUpdate == result

def test_completeOrderStatus(statusTester):
    statusTester.completeOrderStatus()
    result = statusTester.complete
    assert result == True

def test_addToOrder(orderTester, orderItemTester):
    orderTester.addToOrder(orderItemTester)
    assert any(orderTester.items, orderItemTester)

def test_removeFromOrder(orderTester, orderItemTester):
    orderTester.addToOrder(orderItemTester)
    orderTester.removeFromOrder(orderItemTester)
    assert any(orderTester.items, orderItemTester) == False

def test_sendOrder(orderTester):
    orderTester.sendOrder()
    result = orderTester.sent
    assert result

