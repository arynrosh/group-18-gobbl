import requests

rest_url = ""
#need to refind the link from canvas

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