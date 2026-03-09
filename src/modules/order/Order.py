import requests
import json
import mysql.connector
import fastAPI

#Task 4.1: Design database tables for Orders, Order Items, and Status Tracking
#Task 4.2: Implement API to create, modify, and submit orders (cart system)
#Task 4.3: Implement logic to prevent modifications after order completion
#Task 4.4: Implement API to fetch order status for a customer or restaurant
#Task 4.5: Unit tests for order creation, modification, and status updates

#need to figure out how to connect to the online database provided
try: 
    gobbl = mysql.connector.connect(
    host="localhost",
    user="Group18",
    password="Gobbl"
    )
except:
    print("Could not connect to database")

db = "https://www.kaggle.com/datasets/niszarkiah/food-delivery"
#don't know how to get it to give all info under the columns
parameters = {"order_id", "food_item", "resturant_id", "order_value"}
response = requests.get(db, parameters)

gobblcursor = gobbl.cursor()

gobblcursor.execute("CREATE TABLE food (name VARCHAR(50), restID SMALLINT(3), price FLOAT(9, 2))")

#not sure how to add in an array for the individual items, or python classes
gobblcursor.execute("CREATE TABLE order (orderID CHAR(7), custName VARCHAR(50), totalPrice FLOAT(9, 2))")

gobblcursor.execute("CREATE TABLE status (orderID CHAR(7), current VARCHAR(20), complete BOOL)")

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

        gobblcursor.execute(sql)

for i in response:
    #figure out how to get the info by row

    
    foodItem = new orderItem(i.food_item, i.order_value, i.resturant_id)

class order:
    orderID = ""
    custName = ""
    sent = False
    foods = []
    orderPrice = 0.00

    def __init__(self, oID, cNam):
        self.orderID = oID
        self.custName = cNam

    def add(item: orderItem):
        #I don't know why it doesn't recognize things in its own class
        if sent == false:
            foods.append(item)
            orderPrice = 0.00
            getPrice()
    
    def remove(item: orderItem):
        #I don't know why it doesn't recognize things in its own class
        if sent == false:
            foods.remove(orderItem)
            orderPrice = 0.00
            getPrice()

    def getPrice():
        for i in foods:
            orderPrice += foods.price
        return orderPrice

    def sendOrder():
        getPrice()
        #billing process
        #Have it equal a finalPrice

        #order table
        sql = "INSERT INTO order (orderID, custName, totalPrice) VALUES (%s, %s, %s)"
        val = (orderID, custName, finalPrice)
        tempcursor.execute(sql)
       
        #statusTable
        sql2 = "INSERT INTO status (orderID, current, complete) VALUES (%s, %s, %s)"
        val = (orderID, "Sent", False)
        ordStat = new status(orderID)
        tempcursor.execute(sql2)

        sent = true
        return sent

class status:
    orderID = ""
    current = ""
    complete = False

    def __init__(self, oID):
        self.orderID = oID
        self.current = "Sent"

    def updateOrder(stat):
        if complete == False:
            current = stat
        else:
            return "A completed order can not be updated"
        
    def complOrd():
        complete = True

