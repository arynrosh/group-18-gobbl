import requests
import json
import mysql.connector
from fastapi import fastAPI
import pytest

#Task 4.1: Design database tables for Orders, Order Items, and Status Tracking
#Task 4.2: Implement API to create, modify, and submit orders (cart system)
#Task 4.3: Implement logic to prevent modifications after order completion
#Task 4.4: Implement API to fetch order status for a customer or restaurant
#Task 4.5: Unit tests for order creation, modification, and status updates

try: 
    gobbl = mysql.connector.connect(
    host="localhost",
    user="Group18",
    password="Gobbl"
    )
except:
    print("Could not connect to database")

db = "src\modules\order\food_delivery.csv" #might have path changed after
#don't know how to get it to give all info under the columns
parameters = {"order_id", "food_item", "resturant_id", "order_value"}
try:
    response = requests.get(db, parameters)
    data = response.json()
except:
    print("Could not connect to Kaggle database")

gobblResult = data.fetchall()
for i in gobblResult:
    #figure out how to get the info by row

    foodItem = orderItem(i.food_item, i.order_value, i.resturant_id)

gobblcursor = gobbl.cursor()

gobblcursor.execute("CREATE TABLE food (name VARCHAR(50), restID SMALLINT(3), price FLOAT(9, 2))")

gobblcursor.execute("CREATE TABLE order (orderID CHAR(7), custName VARCHAR(50), totalPrice FLOAT(9, 2))")

gobblcursor.execute("CREATE TABLE status (orderID CHAR(7), current VARCHAR(20), complete BOOL)")

class orderItem:

    def __init__(self, nam: str, pri: int, rID: int):
        self.name = nam
        self.price = pri
        self.restID = rID

        sql = "INSERT INTO food (name, restID, price) VALUES (%s, %s, %s)"
        val = (nam, rID, pri)

        gobblcursor.execute(sql)
    
    def getName(self):
        return self.name
    
    def getRestid(self):
        return self.restID
    
    def getPrice(self):
        return self.price




class order:

    def __init__(self, oID, cNam):
        self.orderID = oID
        self.custName = cNam
        self.sent = False
        self.foods = []
        self.orderPrice = 0.00

    def add(self, item: orderItem):
        #I don't know why it doesn't recognize things in its own class
        if self.sent == False:
            self.foods.append(item)
            self.orderPrice = 0.00
            self.getPrice()
    
    def remove(self, item: orderItem):
        #I don't know why it doesn't recognize things in its own class
        if self.sent == False:
            self.foods.remove(orderItem)
            self.orderPrice = 0.00
            self.getPrice()

    def getPrice(self):
        for i in self.foods:
            self.orderPrice += i.price
        return self.orderPrice

    def sendOrder(self):
        self.getPrice(self)
        #billing process
        #Have it equal a finalPrice

        #order table
        sql = "INSERT INTO order (orderID, custName, totalPrice) VALUES (%s, %s, %s)"
        val = (self.orderID, self.custName, finalPrice) #finalPrice is a placeholder for now
        gobblcursor.execute(sql)
       
        #statusTable
        sql2 = "INSERT INTO status (orderID, current, complete) VALUES (%s, %s, %s)"
        val = (self.orderID, "Sent", False)
        ordStat = status(self.orderID)
        gobblcursor.execute(sql2)

        self.sent = True
        return self.sent

class status:
    def __init__(self, oID: str):
        self.orderID = oID
        self.current = "Sent"
        self.complete = False

    def updateOrder(self, stat):
        if self.complete == False:
            self.current = stat
            return self.current
        else:
            return "A completed order can not be updated"
        
    def complOrd(self):
        self.complete = True
        return self.complete

