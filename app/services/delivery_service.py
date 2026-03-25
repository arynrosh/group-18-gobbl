import json
import os
from pathlib import Path
from typing import Dict, Any, List
from fastapi import HTTPException, status
from app.schemas.delivery import DriverDistanceUpdate, DriverStatusUpdate
from app.repositories.drivers_repo import (
    load_all_drivers,
    save_all_drivers
)

ORDER_PATH = Path(__file__).resolve().parents[1] / "data" / "mock_data" / "orders_mock.json"

def load_all_orders() -> List[Dict[str, Any]]:
    if not ORDER_PATH.exists():
        return []
    
    with ORDER_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def save_all_orders(drivers: List[Dict[str, Any]]) -> None:
    tmp = ORDER_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(drivers, f, ensure_ascii=False, indent=2)

    os.replace(tmp, ORDER_PATH)    
    
def get_driver_or_404(driver_id: int) -> dict:
    drivers = load_all_drivers()
    for  driver in drivers:
        if driver["driver_id"] == driver_id:
            return driver, drivers
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Driver with id {driver_id} not found"
    )
    
def get_order_or_404(order_id: str) -> Dict[str, Any]:
    orders = load_all_orders()
    for order in orders:
        if order["order_id"] == order_id:
            return order, orders
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with id {order_id} not found"
    )

def update_driver_distance(driver_id: int, driver_data: DriverDistanceUpdate) -> dict:
    driver, drivers = get_driver_or_404(driver_id)

    driver["driver_distance"] = driver_data.driver_distance
    save_all_drivers(drivers)

    return driver

def update_driver_status(driver_id: int, driver_data: DriverStatusUpdate) -> dict:
    allowed_statuses = {"available", "busy"}
    if driver_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {allowed_statuses}"
        )
    
    driver, drivers = get_driver_or_404(driver_id)
    driver["status"] = driver_data.status
    save_all_drivers(drivers)

    return driver

def find_nearest_available_driver(order_id: str) -> dict:
    order, _ = get_order_or_404(order_id)
    drivers = load_all_drivers()

    target_distance = order["delivery_distance"]
    nearest_driver = None
    min_distance = float("inf")

    for driver in drivers:
        if driver["status"] != "available":
            continue
    
        driver_distance = driver["driver_distance"]
        difference = abs(driver_distance - target_distance)
        if difference < min_distance:
            min_distance = difference
            nearest_driver = driver

    if not nearest_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available drivers found"
        )
    
    return nearest_driver

def assign_driver_to_order(order_id: str, driver_id: int, auto: bool = False) -> dict:
    order, orders = get_order_or_404(order_id)
    driver, drivers = get_driver_or_404(driver_id)

    if order["assigned_driver_id"] is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already has an assigned driver"
        )

    if driver["status"] != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driver is not available"
        )
    
    order["assigned_driver_id"] = driver_id
    driver["status"] = "busy"

    save_all_orders(orders)
    save_all_drivers(drivers)

    if auto:
        return {
            "message": f"Driver {driver['name']} automatically assigned to order {order_id}",
            "order": order,
            "driver": driver
        }
    else:
        return {
            "message": f"Driver {driver['name']} assigned to order {order_id}",
            "order": order,
            "driver": driver
        }

def auto_assign_driver(order_id: str) -> dict:
    nearest_driver = find_nearest_available_driver(order_id) 
    return assign_driver_to_order(order_id, nearest_driver["driver_id"], True)