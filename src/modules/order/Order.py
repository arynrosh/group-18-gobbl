import requests
import json
import mysql.connector

#Task 4.1: Design database tables for Orders, Order Items, and Status Tracking
#Task 4.2: Implement API to create, modify, and submit orders (cart system)
#Task 4.3: Implement logic to prevent modifications after order completion
#Task 4.4: Implement API to fetch order status for a customer or restaurant
#Task 4.5: Unit tests for order creation, modification, and status updates

#need to figure out how to connect to the online database provided
temp = mysql.connector.connect(
  host="localhost",
  user="Group18",
  password="Gobbl"
) 

tempcursor = temp.cursor()

tempcursor.execute("CREATE TABLE food (name VARCHAR(50), restID SMALLINT(3), price FLOAT(9, 2))")

#not sure how to add in an array for the individual items
tempcursor.execute("CREATE TABLE order (orderID VARCHAR(7), custName VARCHAR(50), totalPrice FLOAT(9, 2))")

tempcursor.execute("CREATE TABLE status (orderID VARCHAR(7), complete BOOL)")

class orderItem:
    name = ""
    price = 0.00
    restID = 0

    def __init__(self, nam, pri, rID):
        self.name = nam
        self.price = pri
        self.restID = rID

        sql = "INSERT INTO food (name, restID, price) VALUES (%s, %s, %s)"
        val = (nam, rID, pri)

        tempcursor.execute(sql)

class order:
    orderID = ""
    custName = ""
    sent = False
    foods = []
    totalPrice = 0.00

    def __init__(self, oID, cNam):
        self.orderID = oID
        self.custName = cNam

    def add(item: orderItem):
        #I don't know why it doesn't recognize things in its own class
        if sent == false:
            foods.append(item)
            totalPrice = 0.00
            getPrice()
    
    def remove(item: orderItem):
        #I don't know why it doesn't recognize things in its own class
        if sent == false:
            foods.remove(orderItem)
            totalPrice = 0.00
            getPrice()

    def getPrice():
        for i in foods:
            totalPrice += foods.price

    def sendOrder():
        getPrice()
        #billing process
        sent = true

