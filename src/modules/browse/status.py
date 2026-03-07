import requests

datab_url = "https://www.kaggle.com/datasets/niszarkiah/food-delivery"

def orderStatus():
    status = str(input("Order Status for"))
    url = f"{datab_url}/{status}"
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