import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.services.order_service import App
from app.schemas.order import Order, OrderItem, Status
#app\services\order_service.py
from app.services.order_service import updateStatus, getStatusCurrent, completeOrderStatus, getStatusComplete, addToOrder, removeFromOrder, sendOrder, getOrderSent, getOrderItems

client2 = TestClient(App)

"""
@pytest.fixture
def statusTester():
    stat=Status()
    stat.order_id = "123456"
    stat.current = "sent"
    stat.complete = False
    
    return stat
"""
@pytest.fixture
def statusTester():
    return Status(
        order_id="123456",
        current="sent",   # or the correct member
        complete=False,
    )

@pytest.fixture
def orderItemTester():
    return OrderItem(
        food_item = "Tacos",
        quantity = 1,
        order_value = 12.99,
        resturant_id = 13
    )

@pytest.fixture
def orderTester():
    return Order(
        order_id = "123456",
        customer_id = "gertrude",
        restaurant_id = 13,
        items = [orderItemTester],
        sent = False
    )


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
