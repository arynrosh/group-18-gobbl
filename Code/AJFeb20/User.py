//import mysql.connector 
//resolve later

from abc import ABC, abstractmethod
class User {
    users = mysql.connector.connect(
        host="localhost",
        user="gobbl",
        password="group18"
    )

    usercursor = user.cursor()

    usercursor.execute("CREATE DATABASE users")

    usercursor.execute("CREATE TABLE user (type VARCHAR(9), username VARCHAR(20), password VARCHAR(), makeOrder BOOLEAN, collectOrder BOOLEAN, recieveOrder BOOLEAN)")

}