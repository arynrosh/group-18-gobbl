import requests
import json
from fastapi import HTTPException
import pytest
from app.schemas.order import OrderItem, Order, Status

#Order = fastAPI()

#Task 4.1: Design database tables for Orders, Order Items, and Status Tracking
#Task 4.2: Implement API to create, modify, and submit orders (cart system)
#Task 4.3: Implement logic to prevent modifications after order completion
#Task 4.4: Implement API to fetch order status for a customer or restaurant
#Task 4.5: Unit tests for order creation, modification, and status updates

#FastAPI lab presentation 

"""db = "app/data/food_delivery.csv"
parameters = {"order_id", "food_item", "resturant_id", "order_value"}
try:
    response = requests.get(db, parameters)
    data = response.json()
except:
    print("Could not connect to Kaggle database")"""

"""class orderItem:

    def __init__(self, nam: str, pri: int, rID: int):
        self.name = nam
        self.price = pri
        self.restID = rID
    
    def getName(self):
        return self.name
    
    def getRestid(self):
        return self.restID
    
    def getPrice(self):
        return self.price
    
    def toString(self):
        return "Name: " + self.name + ", price: " + self.price + ", resturant ID: " + self.restID"""

def addToOrder(orderItem: OrderItem) -> Order:
    if Order.sent == False:
        Order.items.append(orderItem)

def removeFromOrder(orderItem: OrderItem) -> Order:
    if Order.sent == False:
            if any(Order.foods, orderItem):
                Order.foods.remove(orderItem)

def sendOrder(orderId: str) -> Order:
    Order.sent = True

"""class order:

    def __init__(self, oID: str, cNam: str):
        self.orderID = oID
        self.custName = cNam
        self.sent = False
        self.foods = []
        self.orderPrice = 0.00

    def add(self, item: orderItem):
        if self.sent == False:
            self.foods.append(item)
            #self.orderPrice = 0.00
            #self.getPrice()
    
    def remove(self, item: orderItem):
        if self.sent == False:
            if self.any(self.foods, orderItem):
                self.foods.remove(orderItem)
            #self.orderPrice = 0.00
            #self.getPrice()

    def getPrice(self):
        for i in self.foods:
            self.orderPrice += i.price
        return self.orderPrice

    def showCart(self):
        for i in self.foods:
            print(i.toString())

    def sendOrder(self):
        orderPrice = self.getPrice(self)
        #billing process
        #Have it equal a finalPrice

        self.sent = True
        return self.sent"""

def updateStatus(status: str) -> Status:
    if Status.complete == False:
        current = status

def completeOrderStatus() -> Status:
    Status.complete = True

"""class status:
    def __init__(self, oID: str):
        self.orderID = oID
        self.current = "Sent"
        self.complete = False

    def updateOrder(self, stat: str):
        if self.complete == False:
            self.current = stat
            return self.current
        else:
            return "A completed order can not be updated"
        
    def complOrd(self):
        self.complete = True
        return self.complete"""

