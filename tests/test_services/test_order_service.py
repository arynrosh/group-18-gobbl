import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.services.order_service import App
from app.schemas.order import Order, OrderItem, Status
#app\services\order_service.py
from app.services.order_service import updateStatus, getStatusCurrent, completeOrderStatus, getStatusComplete, addToOrder, removeFromOrder, sendOrder, getOrderSent, getOrderItems

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
    updateStatus(statusTester, "Ready")
    result = getStatusCurrent(statusTester)
    assert statusUpdate == result

def test_completeOrderStatus(statusTester):
    completeOrderStatus(statusTester)
    result = getStatusComplete(statusTester)
    assert result == True

def test_addToOrder(orderTester, orderItemTester):
    addToOrder(orderTester, orderItemTester)
    assert any(getOrderItems(orderTester), orderItemTester)

def test_removeFromOrder(orderTester, orderItemTester):
    addToOrder(orderTester, orderItemTester)
    removeFromOrder(orderTester, orderItemTester)
    assert any(getOrderItems(orderTester), orderItemTester) == False

def test_sendOrder(orderTester):
    sendOrder(orderTester)
    result = getOrderSent(orderTester)
    assert result

