import mysql.connector
#resolve later

from abc import ABC, abstractmethod
class User :

    users = mysql.connector.connect(
        host="localhost",
        user="root",
        password="group18"
    )

    usercursor = users.cursor()

    usercursor.execute("CREATE DATABASE users")

    usercursor.execute("CREATE TABLE user (type VARCHAR(9), username VARCHAR(20), password VARCHAR(), custPermissions BOOLEAN, drivPermissions BOOLEAN, restPermissions BOOLEAN)")
    #Just Going with blanket permissions for the classes as they will be the same for all of those within their type
    #Apparently we don't need to make any databases for this, so I'll be making a stock customer, driver, resturant and maybe admin




class Login :
    username = "   "
    password = "   "

    def log(user, passw):

