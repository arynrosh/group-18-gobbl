import pytest
from fastapi import HTTPException
from app.services import delivery_service

def reset_test_data():
    delivery_service.drivers_db.clear()
    delivery_service.drivers_db.update({
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
    })

    delivery_service.deliveries_db.clear()
    delivery_service.deliveries_db.update({
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
    })

def setup_function():
    reset_test_data()

def test_calculate_distance():
    dist = delivery_service.calculate_distance(0, 0, 3, 4)
    assert dist == 5.0

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

def test_get_delivery_or_404_raises_exception_for_missing_delivery():
    with pytest.raises(HTTPException) as exc:
        delivery_service.get_delivery_or_404("missing_delivery")
    assert exc.value.status_code == 404
    assert exc.value.detail == "Delivery not found"

def test_update_driver_location():
    driver = delivery_service.update_driver_location("driver1", 7.5, 8.5)
    assert driver["location"]["x"] == 7.5
    assert driver["location"]["y"] == 8.5

def test_update_driver_status_to_busy():
    driver = delivery_service.update_driver_status("driver1", "busy")
    assert driver["status"] == "busy"

def test_update_driver_status_invalid_value():
    with pytest.raises(HTTPException) as exc:
        delivery_service.update_driver_status("driver1", "offline")
    assert exc.value.status_code == 400

def test_find_nearest_available_driver():
    nearest = delivery_service.find_nearest_available_driver("delivery1")
    assert nearest["id"] == "driver3"  # Eve should be selected as she's the closest available driver

def test_find_nearest_available_driver_no_available():
    delivery_service.update_driver_status("driver1", "busy")
    delivery_service.update_driver_status("driver3", "busy")
    with pytest.raises(HTTPException) as exc:
        delivery_service.find_nearest_available_driver("delivery1")
    assert exc.value.status_code == 404
    assert exc.value.detail == "No available drivers found"

def test_auto_assign_driver():
    result = delivery_service.auto_assign_driver("delivery1")
    assert result["delivery"]["assigned_driver_id"] == "driver3"
    assert result["driver"]["id"] == "driver3"
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

def test_assign_driver_to_delivery_driver_busy():
    with pytest.raises(HTTPException) as exc:
        delivery_service.assign_driver_to_delivery("delivery2", "driver2")
    assert exc.value.status_code == 400
    assert exc.value.detail == "Driver is not available"