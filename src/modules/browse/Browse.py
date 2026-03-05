import requests

rest_url = "https://www.kaggle.com/datasets/niszarkiah/food-delivery"
#should be attached to the app
orderinfo = ""

def searchBar():
    food = str(input("Search for"))
    url = f"{rest_url}/{food}" # will only work if it fully matches the url
    response = requests.get(url)
    if response.status_code == 200:
        print("Item found")
        desiredFood = response.json() # gets the information
        return desiredFood
    else:
        print("Item not found")



def orderStatus():
    status = str(input("Order Status for"))
    url = f"{orderinfo}/{status}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Status found")
        stat = response.json()
        return stat
    else:
        print("Order Not Found")



#example of how to change branch
# C:\Users\aylaj\OneDrive\Desktop\COSC310Project\group-18-gobbl> git checkout -b ayla/tasks1.1      
#Switched to a new branch 'ayla/tasks1.1'
