import pytest
import json
from fastapi import HTTPException
from app.services import delivery_service

def reset_test_data():
    delivery_service.drivers_db.clear()
    with open("app/data/drivers.json", mode="r", encoding="utf-8") as file:
        drivers = json.load(file)
        for driver in drivers:
            delivery_service.drivers_db[driver["id"]] = driver

    delivery_service.deliveries_db.clear()
    delivery_service.deliveries_db.update({
        "delivery1": {
            "id": "delivery1",
            "restaurant_id": "rest1",
            "delivery_distance": 5.0,
            "assigned_driver_id": None,
        },
        "delivery2": {
            "id": "delivery2",
            "restaurant_id": "rest2",
            "delivery_distance": 8.0,
            "assigned_driver_id": None,
        }
    })

def setup_function():
    reset_test_data()

def test_get_driver_or_404_returns_driver():
    driver = delivery_service.get_driver_or_404("driver1")
    assert driver["name"] == "Charlie"

def test_get_driver_or_404_raises_exception_for_missing_driver():
    with pytest.raises(HTTPException) as exc:
        delivery_service.get_driver_or_404("missing_driver")
    assert exc.value.status_code == 404
    assert exc.value.detail == "Driver not found"

def test_get_delivery_or_404_returns_delivery():
    delivery = delivery_service.get_delivery_or_404("delivery1")
    assert delivery["restaurant_id"] == "rest1"
    assert delivery["delivery_distance"] == 5.0

def test_get_delivery_or_404_raises_exception_for_missing_delivery():
    with pytest.raises(HTTPException) as exc:
        delivery_service.get_delivery_or_404("missing_delivery")
    assert exc.value.status_code == 404
    assert exc.value.detail == "Delivery not found"

def test_update_driver_distance():
    driver = delivery_service.update_driver_distance("driver1", 7.5)
    assert driver["driver_distance"] == 7.5

def test_update_driver_status_to_busy():
    driver = delivery_service.update_driver_status("driver1", "busy")
    assert driver["status"] == "busy"

def test_update_driver_status_invalid_value():
    with pytest.raises(HTTPException) as exc:
        delivery_service.update_driver_status("driver1", "invalid_status")
    assert exc.value.status_code == 400

def test_find_nearest_available_driver():
    nearest = delivery_service.find_nearest_available_driver("delivery1")
    assert nearest["id"] == "driver1"

def test_find_nearest_available_driver_no_available():
    delivery_service.update_driver_status("driver1", "busy")
    delivery_service.update_driver_status("driver3", "busy")
    with pytest.raises(HTTPException) as exc:
        delivery_service.find_nearest_available_driver("delivery1")
    assert exc.value.status_code == 404
    assert exc.value.detail == "No available drivers found"

def test_auto_assign_driver():
    result = delivery_service.auto_assign_driver("delivery1")
    assert result["delivery"]["assigned_driver_id"] == "driver1"
    assert result["driver"]["id"] == "driver1"
    assert result["driver"]["status"] == "busy"

def test_assign_driver_to_delivery():
    result = delivery_service.assign_driver_to_delivery("delivery2", "driver1")
    assert result["delivery"]["assigned_driver_id"] == "driver1"
    assert result["driver"]["id"] == "driver1"
    assert result["driver"]["status"] == "busy"

def test_assign_driver_to_delivery_already_assigned():
    delivery_service.assign_driver_to_delivery("delivery1", "driver1")
    with pytest.raises(HTTPException) as exc:
        delivery_service.assign_driver_to_delivery("delivery1", "driver3")
    assert exc.value.status_code == 400
    assert exc.value.detail == "Delivery already has an assigned driver"

def test_assign_driver_to_delivery_driver_busy_or_offline():
    with pytest.raises(HTTPException) as exc:
        delivery_service.assign_driver_to_delivery("delivery2", "driver2")
    assert exc.value.status_code == 400
    assert exc.value.detail == "Driver is not available"

def test_csv_loaded_deliveries_have_delivery_distance():
    for delivery in delivery_service.deliveries_db.values():
        assert "delivery_distance" in delivery

def test_csv_loaded_drivers_are_not_empty():
    assert len(delivery_service.drivers_db) > 0