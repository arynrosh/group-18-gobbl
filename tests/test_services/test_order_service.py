import pytest
from fastapi.testclient import TestClient
from app.services.order_service import App
from app.main import app
from app.schemas.order import Order, OrderItem, Status
#app\services\order_service.py
from app.services.order_service import updateStatus, completeOrderStatus, addToOrder, removeFromOrder, sendOrder

client = TestClient(app)
client2 = TestClient(App)

#testing methods for status class
statusTester = Status("1d8e87M")

def test_updateStatus():
    statUpdate = "Ready"
    result = statusTester.updateStatus("Ready")
    assert statUpdate == result

def test_completeOrderStatus():
    result = statusTester.completeOrderStatus()
    assert result == True

#testing methods for orderItem
foodName = "Tacos"
foodPrice = 12.99
foodRid = 13
orderItemTester = OrderItem(foodName, foodPrice, foodRid)

#testing methods for order
orderTester = Order("2f9r98Z", "custest")

def test_addToOrder():
    orderTester.addToOrder(orderItemTester)
    assert any(orderTester.foods, orderItemTester)

def test_removeFromOrder():
    orderTester.addToOrder(orderItemTester)
    orderTester.removeFromOrder(orderItemTester)
    assert any(orderTester.foods, orderItemTester) == False

def test_sendOrder():
    result = orderTester.sendOrder()
    assert result

