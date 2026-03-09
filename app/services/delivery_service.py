from fastapi import HTTPException, status
from math import sqrt

drivers_db = {
    "driver1": {
        "id": "driver1",
        "name": "Charlie",
        "status": "available",
        "location": {"x": 0.0, "y": 0.0}
    },
    "driver2": {
        "id": "driver2",
        "name": "Dave",
        "status": "busy",
        "location": {"x": 5.0, "y": 5.0}
    },
    "driver3": {
        "id": "driver3",
        "name": "Eve",
        "status": "available",
        "location": {"x": 2.0, "y": 1.0}
    }
}

deliveries_db = {
    "delivery1": {
        "id": "delivery1",
        "restaurant_id": "rest1",
        "destination": {"x": 3.0, "y": 4.0},
        "assigned_driver_id": None,
    },
    "delivery2": {
        "id": "delivery2",
        "restaurant_id": "rest2",
        "destination": {"x": 6.0, "y": 8.0},
        "assigned_driver_id": None,
    }
}

#helper functions
def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

#error handling                
def get_driver_or_404(driver_id:str) -> dict:
    driver = drivers_db.get(driver_id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Driver not found",
        )
    return driver

def get_delivery_or_404(delivery_id:str) -> dict:
    delivery = deliveries_db.get(delivery_id)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Delivery not found",
        )
    return delivery

#update driver location & status
def update_driver_location(driver_id: str, x: float, y: float) -> dict:
    driver = get_driver_or_404(driver_id)
    driver["location"] = {"x": x, "y": y}
    return driver

def update_driver_status(driver_id:str, status_value:str) -> dict:
    allowed_statuses = {"available", "busy"}
    if status_value not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {allowed_statuses}"
        )
    driver = get_driver_or_404(driver_id)
    driver["status"] = status_value
    return driver


#delivery assignment logic
def find_nearest_available_driver(delivery_id: str) -> dict:
    delivery = get_delivery_or_404(delivery_id)
    dest_x = delivery["destination"]["x"]
    dest_y = delivery["destination"]["y"]

    nearest_driver = None
    min_distance = float("inf")

    for driver in drivers_db.values():
        if driver["status"] != "available":
            continue
    
        drx = driver["location"]["x"] 
        dry = driver["location"]["y"]
        distance = calculate_distance(drx, dry, dest_x, dest_y)
        if distance < min_distance:
            min_distance = distance
            nearest_driver = driver

    if not nearest_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available drivers found"
        )
    
    return nearest_driver

def auto_assign_driver(delivery_id: str) -> dict:
        delivery = get_delivery_or_404(delivery_id)
        nearest_driver = find_nearest_available_driver(delivery_id)
        
        delivery["assigned_driver_id"] = nearest_driver["id"]
        nearest_driver["status"] = "busy"

        return {
            "message": f"Driver {nearest_driver['name']} automatically assigned to delivery {delivery_id}",
            "delivery": delivery,
            "driver": nearest_driver
        }

def assign_driver_to_delivery(delivery_id: str, driver_id: str) -> dict:
    delivery = get_delivery_or_404(delivery_id)
    driver = get_driver_or_404(driver_id)

    if driver["status"] != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driver is not available"
        )
    
    delivery["assigned_driver_id"] = driver_id
    driver["status"] = "busy"

    return {
        "message": f"Driver {driver['name']} assigned to delivery {delivery_id}",
        "delivery": delivery,
        "driver": driver
    }



    