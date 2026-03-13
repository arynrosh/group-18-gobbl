import pytest
from fastapi.testclient import TestClient
from app.services.order_service import Order, OrderItem, Status
#app\services\order_service.py

client = TestClient(Order)

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

"""def test_getName():
    result = orderItemTester.getName()
    assert result == foodName

def test_getPrice():
    result = orderItemTester.getPrice()
    assert result == foodPrice

def test_getRestid():
    result = orderItemTester.getRestid()
    assert result == foodRid

def test_toString():
    result = orderItemTester.toString()
    expected = "Name: " + foodName + ", price: " + foodPrice + ", resturant ID: " + foodRid
    assert result == expected"""

#testing methods for order
orderTester = Order("2f9r98Z", "custest")

def test_addToOrder():
    orderTester.addToOrder(orderItemTester)
    assert any(orderTester.foods, orderItemTester)

def test_removeFromOrder():
    orderTester.addToOrder(orderItemTester)
    orderTester.removeFromOrder(orderItemTester)
    assert any(orderTester.foods, orderItemTester) == False

"""def test_getPrice():
    orderTester.addToOrder(orderItemTester)
    orderTester.addToOrder(orderItemTester)
    expected = foodPrice * 2 #25.98
    result = orderTester.getPrice()
    assert expected == result"""

def test_sendOrder():
    result = orderTester.sendOrder()
    assert result

