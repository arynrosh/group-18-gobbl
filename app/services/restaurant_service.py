import csv
from typing import List
# andrea i think i messed up the merge for the schemas file, should be an easy fix if you just move your part to a restaurant schemas file and then import it here
from app.schemas.menu import Restaurant

restaurants = []

with open("app/data/restaurants.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        restaurants.append({
            "id": int(row["restaurant_id"]),
            "name": row["name"],
            "cuisine": row["cuisine"],
            "location": row["location"]
        })

def search_by_name(name: str) -> List[Restaurant]:
    
    results = []
    for restaurant in restaurants:
        if name.lower() in restaurant["name"].lower():
            results.append(Restaurant(**restaurant))
    return results

def search_by_cuisine(cuisine: str) -> List[Restaurant]:
    
    results = []
    for restaurant in restaurants:
        if cuisine.lower() in restaurant["cuisine"].lower():
            results.append(Restaurant(**restaurant))
    return results