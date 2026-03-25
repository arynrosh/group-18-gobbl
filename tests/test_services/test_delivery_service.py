import pytest
from pydantic import ValidationError
import json
from fastapi import HTTPException
from unittest.mock import patch
from app.services import delivery_service
from app.schemas.delivery import DriverDistanceUpdate, DriverStatusUpdate

FAKE_DRIVERS = [
    {
        "id": 1,
        "name": "A",
        "status": "available",
        "driver_distance": 5.0
    }, 
    {
        "id": 2,
        "name": "B",
        "status": "busy",
        "driver_distance": 3.0
    },
    {
        "id": 3,
        "name": "C",
        "status": "available",
        "driver_distance": 8.0
    }
]

BUSY_DRIVERS = [
    {
        "id": 1,
        "name": "A",
        "status": "busy",
        "driver_distance": 5.0
    }, 
    {
        "id": 2,
        "name": "B",
        "status": "busy",
        "driver_distance": 3.0
    },
    {
        "id": 3,
        "name": "C",
        "status": "busy",
        "driver_distance": 8.0
    }
]

FAKE_ORDERS = [{
  "order_id": "cust-odr-1",
  "customer_id": "some-customer-id-1",
  "restaurant_id": 53,
  "delivery_distance": 5.0,
  "assigned_driver_id": None,
  "items": [
    {
        "menu_item_id": 1,
        "food_item": "Burger",
        "order_value": 41.17

    }
  ]
},
{
  "order_id": "cust-odr-2",
  "customer_id": "some-customer-id-2",
  "restaurant_id": 3,
  "delivery_distance": 8.0,
  "assigned_driver_id": 2,
  "items": [
    {
        "menu_item_id": 2,
        "food_item": "Pasta",
        "order_value": 37.25

    }
  ]
}]

def test_get_driver_or_404_returns_driver():
    with patch("app.services.delivery_service.load_all_drivers", return_value=FAKE_DRIVERS):
        driver, drivers = delivery_service.get_driver_or_404(1)
        assert driver["name"] == "A"
        assert len(drivers) == 3

def test_get_driver_or_404_raises_exception_for_missing_driver():
    with patch("app.services.delivery_service.load_all_drivers", return_value=FAKE_DRIVERS):
        with pytest.raises(HTTPException) as exc:
            delivery_service.get_driver_or_404(999)
        assert exc.value.status_code == 404
        assert exc.value.detail == "Driver with id 999 not found"

def test_get_order_or_404_returns_order():
    with patch("app.services.delivery_service.load_all_orders", return_value=FAKE_ORDERS):
        order, orders = delivery_service.get_order_or_404("cust-odr-1")
        assert order["restaurant_id"] == 53
        assert order["delivery_distance"] == 5.0
        assert len(orders) == 2

def test_get_order_or_404_raises_exception_for_missing_order():
    with patch("app.services.delivery_service.load_all_orders", return_value=FAKE_ORDERS):
        with pytest.raises(HTTPException) as exc:
            delivery_service.get_order_or_404("missing-order")
    assert exc.value.status_code == 404
    assert exc.value.detail == "Order with id missing-order not found"

def test_update_driver_distance():
    fake_drivers = [driver.copy() for driver in FAKE_DRIVERS]
    with patch("app.services.delivery_service.load_all_drivers", return_value=fake_drivers), \
        patch("app.services.delivery_service.save_all_drivers") as mock_save:
        driver_data = DriverDistanceUpdate(driver_distance=7.5)
        driver = delivery_service.update_driver_distance(1, driver_data)
        
        assert driver["driver_distance"] == 7.5
        mock_save.assert_called_once()

def test_update_driver_distance_raises_400_for_negative_distance():
    with pytest.raises(ValidationError):
        DriverDistanceUpdate(driver_distance=-1.0)

def test_update_driver_status_to_busy():
    fake_drivers = [driver.copy() for driver in FAKE_DRIVERS]
    with patch("app.services.delivery_service.load_all_drivers", return_value=fake_drivers), \
        patch("app.services.delivery_service.save_all_drivers") as mock_save:
        driver_data = DriverStatusUpdate(status="busy")
        driver = delivery_service.update_driver_status(1, driver_data)
        
        assert driver["status"] == "busy"
        mock_save.assert_called_once()    

def test_update_driver_status_invalid_value():
    fake_drivers = [driver.copy() for driver in FAKE_DRIVERS]
    with patch("app.services.delivery_service.load_all_drivers", return_value=fake_drivers), \
        patch("app.services.delivery_service.save_all_drivers") as mock_save:
        driver_data = DriverStatusUpdate(status="offline")
        
        with pytest.raises(HTTPException) as exc:
            delivery_service.update_driver_status("1", driver_data)
        
    assert exc.value.status_code == 400
    assert "Status must be one of" in exc.value.detail  

def test_find_nearest_available_driver():
    with patch("app.services.delivery_service.load_all_drivers", return_value=FAKE_DRIVERS), \
        patch("app.services.delivery_service.load_all_orders", return_value=FAKE_ORDERS):
        nearest = delivery_service.find_nearest_available_driver("cust-odr-1")
        assert nearest["id"] == 1

def test_find_nearest_available_driver_no_available():
    with patch("app.services.delivery_service.load_all_drivers", return_value=BUSY_DRIVERS), \
        patch("app.services.delivery_service.load_all_orders", return_value=FAKE_ORDERS):
        with pytest.raises(HTTPException) as exc:
            delivery_service.find_nearest_available_driver("cust-odr-1")
    assert exc.value.status_code == 404
    assert exc.value.detail == "No available drivers found"

def test_auto_assign_driver():
    fake_drivers = [driver.copy() for driver in FAKE_DRIVERS]
    fake_orders = [order.copy() for order in FAKE_ORDERS]
    fake_orders[0]["assigned_driver_id"] = None

    with patch("app.services.delivery_service.load_all_drivers", return_value=fake_drivers), \
        patch("app.services.delivery_service.load_all_orders", return_value=fake_orders), \
        patch("app.services.delivery_service.save_all_orders", return_value=fake_orders), \
        patch("app.services.delivery_service.save_all_drivers") as mock_save_drivers, \
        patch("app.services.delivery_service.save_all_orders") as mock_save_orders:
        result = delivery_service.auto_assign_driver("cust-odr-1")

        assert result["order"]["assigned_driver_id"] == 1
        assert result["driver"]["id"] == 1
        assert result["driver"]["status"] == "busy"
        mock_save_drivers.assert_called_once()
        mock_save_orders.assert_called_once()

def test_assign_driver_to_order():
    fake_drivers = [driver.copy() for driver in FAKE_DRIVERS]
    fake_orders = [order.copy() for order in FAKE_ORDERS]
    fake_orders[0]["assigned_driver_id"] = None

    with patch("app.services.delivery_service.load_all_drivers", return_value=fake_drivers), \
        patch("app.services.delivery_service.load_all_orders", return_value=fake_orders), \
        patch("app.services.delivery_service.save_all_orders", return_value=fake_orders), \
        patch("app.services.delivery_service.save_all_drivers") as mock_save_drivers, \
        patch("app.services.delivery_service.save_all_orders") as mock_save_orders:
        result = delivery_service.assign_driver_to_order("cust-odr-1", 1)

        assert result["order"]["assigned_driver_id"] == 1
        assert result["driver"]["id"] == 1
        assert result["driver"]["status"] == "busy"
        mock_save_drivers.assert_called_once()
        mock_save_orders.assert_called_once()

def test_assign_driver_to_delivery_already_assigned():
    fake_drivers = [driver.copy() for driver in FAKE_DRIVERS]
    fake_orders = [order.copy() for order in FAKE_ORDERS]
    fake_orders[0]["assigned_driver_id"] = 1

    with patch("app.services.delivery_service.load_all_drivers", return_value=fake_drivers), \
        patch("app.services.delivery_service.load_all_orders", return_value=fake_orders):
            with pytest.raises(HTTPException) as exc:
                delivery_service.assign_driver_to_order("cust-odr-1", 3)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Order already has an assigned driver"

def test_assign_driver_to_delivery_driver_busy_or_offline():
    fake_drivers = [driver.copy() for driver in FAKE_DRIVERS]
    fake_orders = [order.copy() for order in FAKE_ORDERS]

    with patch("app.services.delivery_service.load_all_drivers", return_value=fake_drivers), \
        patch("app.services.delivery_service.load_all_orders", return_value=fake_orders):
            with pytest.raises(HTTPException) as exc:
                delivery_service.assign_driver_to_order("cust-odr-1", 2)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Driver is not available"