import csv
from typing import List
from app.schemas.restaurant import Restaurant

restaurants = []

with open("data/restaurants.csv", newline="") as f:
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