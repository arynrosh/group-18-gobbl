import requests

rest_url = "https://www.kaggle.com/datasets/niszarkiah/food-delivery"
#Thank you Drea 

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