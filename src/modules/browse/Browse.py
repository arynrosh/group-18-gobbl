import requests
import json

#Task 4.1: Design database tables for Orders, Order Items, and Status Tracking
#Task 4.2: Implement API to create, modify, and submit orders (cart system)
#Task 4.3: Implement logic to prevent modifications after order completion
#Task 4.4: Implement API to fetch order status for a customer or restaurant
#Task 4.5: Unit tests for order creation, modification, and status updates

rest_url = "https://www.kaggle.com/datasets/niszarkiah/food-delivery"

#should be attached to the app
#orderinfo = ""

def searchBar():
    food = str(input("Search for"))
    url = f"{rest_url}/{food}" # will only work if it fully matches the url
    response = requests.get(url)
    #Needs to search for a food item


    if response.status_code == 200:
        print("Database Found")
        #desiredFood = response.json() # gets the information
        #return desiredFood
    else:
        print("Database not found")




