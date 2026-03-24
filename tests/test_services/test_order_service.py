import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.services.order_service import App
from app.schemas.order import Order, OrderItem, Status
from app.services.order_service import updateStatus, getStatusCurrent, completeOrderStatus, getStatusComplete, addToOrder, removeFromOrder, sendOrder, getOrderSent, getOrderItems

client2 = TestClient(App)

@pytest.fixture
def statusTester():
    return Status(order_id="1234567", current="sent", complete=False)

@pytest.fixture
def orderItemTester():
    return OrderItem(food_item="Tacos", quantity=1, order_value=12.99, resturant_id=13)

@pytest.fixture
def orderItemBackup():
    return OrderItem(food_item="Cheese", quantity=2, order_value=6.66, resturant_id=13)

@pytest.fixture
def orderTester():
    return Order(order_id="123456", customer_id="gertrude", restaurant_id=13, driver_distance=5, assigned_driver_id=2, items=[], sent=False)

def test_updateStatus(statusTester):
    with patch("app.services.order_service.load_all_status", return_value=[statusTester]):
        updateStatus(statusTester, "Ready")
        result = getStatusCurrent(statusTester)
    assert result == "Ready"

def test_completeOrderStatus(statusTester):
     with patch("app.services.order_service.load_all_status", return_value=[statusTester]):
        completeOrderStatus(statusTester)
        result = getStatusComplete(statusTester)
     assert result == True

def test_addToOrder(orderTester, orderItemTester):
    with patch("app.services.order_service.load_all_orders", return_value=[orderTester]):
        addToOrder(orderTester, orderItemTester)
    assert orderTester.items[0] == orderItemTester

def test_removeFromOrder(orderTester, orderItemTester, orderItemBackup):
    with patch("app.services.order_service.load_all_orders", return_value=[orderTester]):
        addToOrder(orderTester, orderItemTester)
        removeFromOrder(orderTester, orderItemTester)
        addToOrder(orderTester, orderItemBackup)
    assert orderTester.items[0] != orderItemTester

def test_sendOrder(orderTester):
    with patch("app.services.order_service.load_all_orders", return_value=[orderTester]):
        sendOrder(orderTester)
    assert orderTester.sent == True

#Copy of command to just run my tests for ease
#pytest tests/test_services/test_order_service.py