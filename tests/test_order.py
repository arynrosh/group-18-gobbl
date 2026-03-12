import pytest
#from fastapi.testclient import TestClient
from src.modules.order import Order
#src\modules\order\Order.py

#testing methods for status class
statusTester = status("1d8e87M")

def test_updateOrder():
    statUpdate = "Ready"
    result = statusTester.updateOrder("Ready")
    assert statUpdate == result

def test_complOrd():
    result = statusTester.compOrd()
    assert result == True

#testing methods for orderItem
foodName = "Tacos"
foodPrice = 12.99
foodRid = 13
orderItemTester = orderItem(foodName, foodPrice, foodRid)

def test_getName():
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
    assert result == expected

#testing methods for order
orderTester = order("2f9r98Z", "custest")

def test_add():
    orderTester.add(orderItemTester)
    assert any(orderTester.foods, orderItemTester)

def test_remove():
    orderTester.add(orderItemTester)
    orderTester.remove(orderItemTester)
    assert any(orderTester.foods, orderItemTester) == False

def test_getPrice():
    orderTester.add(orderItemTester)
    orderTester.add(orderItemTester)
    expected = foodPrice * 2 #25.98
    result = orderTester.getPrice()
    assert expected == result

def test_sendOrder():
    result = orderTester.sendOrder()
    assert result

