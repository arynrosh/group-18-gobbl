import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.services.order_service import App
from app.schemas.order import Order, OrderItem, Status
#app\services\order_service.py
from app.services.order_service import updateStatus, getStatusCurrent, completeOrderStatus, getStatusComplete, addToOrder, removeFromOrder, sendOrder, getOrderSent, getOrderItems

client2 = TestClient(App)

@pytest.fixture
def statusTester():
    stat=Status()
    stat.order_id = "123456"
    stat.current = "sent"
    stat.complete = False
    return stat

@pytest.fixture
def orderItemTester():
    item = OrderItem()
    item.food_item = "Tacos"
    item.quantity = 1
    item.order_value = 12.99
    item.resturant_id = 13
    return item

@pytest.fixture
def orderTester():
    ord = Order()
    ord.order_id = "123456"
    ord.customer_id = "gertrude"
    ord.restaurant_id = 13
    ord.items = [orderItemTester]
    ord.sent = False
    return ord


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
