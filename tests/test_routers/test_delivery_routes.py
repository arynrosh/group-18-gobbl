import json
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch
from app.main import app
from app.services import delivery_service

client = TestClient(app)

def get_token(username: str, password: str) -> str:
    response = client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

FAKE_DRIVER = {
    "id": 1,
    "name": "Charlie",
    "status": "available",
    "driver_distance": 7.0
}

FAKE_BUSY_DRIVER = {
    "id": 1,
    "name": "Charlie",
    "status": "busy",
    "driver_distance": 7.0
}

FAKE_ASSIGN_RESULT = {
    "message": "Driver Charlie assigned to order cust-odr-1",
    "order": {
        "order_id": "cust-odr-1",
        "customer_id": "some-customer-id",
        "restaurant_id": 53,
        "delivery_distance": 5.0,
        "assigned_driver_id": 1,
        "items": [
            {
                "menu_item_id": 1,
                "food_item": "Burger",
                "order_value": 41.17
            }
        ]
    },
    "driver": {
        "id": 1,
        "name": "Charlie",
        "status": "busy",
        "driver_distance": 5.0
    }
}

def test_driver_can_update_distance():
    driver_token =  get_token("dave", "driverpass")

    with patch("app.routers.delivery.update_driver_distance", return_value=FAKE_DRIVER):
        response = client.put("/delivery/drivers/1/driver_distance",
                                json={"driver_distance": 7.0},
                                headers=auth_header(driver_token)
                            )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["driver"]["id"] == 1
    assert data["driver"]["name"] == "Charlie"
    assert data["driver"]["driver_distance"] == 7.0

def test_update_driver_distance_returns_404_when_driver_missing():
    driver_token =  get_token("dave", "driverpass")

    with patch("app.routers.delivery.update_driver_distance",
               side_effect=HTTPException(status_code=404, detail="Driver with id 999 not found")):
                    response = client.put("/delivery/drivers/1/driver_distance",
                                            json={"driver_distance": 7.0},
                                            headers=auth_header(driver_token)
                                        )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Driver with id 999 not found"

def test_update_driver_distance_returns_422_for_negative_distance():
    driver_token =  get_token("dave", "driverpass")
    response = client.put(
          "/delivery/drivers/1/driver_distance",
          json={"driver_distance": "-1.0"},
          headers=auth_header(driver_token)
    )

    assert response.status_code == 422, response.text

def test_driver_can_update_status():
    driver_token = get_token("dave", "driverpass")

    with patch("app.routers.delivery.update_driver_status", return_value=FAKE_BUSY_DRIVER):
        response = client.put("/delivery/drivers/1/driver_status",
                            json = {"status": "busy"},
                            headers=auth_header(driver_token),
                            )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Driver status updated"
    assert data["driver"]["id"] == 1
    assert data["driver"]["status"] == "busy"

def test_driver_can_update_status_returns_400_for_invalid_status():
    driver_token = get_token("dave", "driverpass")

    with patch("app.routers.delivery.update_driver_status", 
               side_effect=HTTPException(status_code=400, detail="Status must be one of: {'available', 'busy'}")):
        response = client.put("/delivery/drivers/1/driver_status",
                            json = {"status": "busy"},
                            headers=auth_header(driver_token),
                            )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Status must be one of: {'available', 'busy'}"

def test_restaurant_owner_can_auto_assign_driver():
    owner_token = get_token("bob", "securepass")

    with patch("app.routers.delivery.auto_assign_driver", return_value=FAKE_ASSIGN_RESULT):
        response = client.post("/delivery/orders/cust-odr-1/auto-assign-driver",
                            headers=auth_header(owner_token),
                            )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["order"]["assigned_driver_id"] == 1

def test_restaurant_owner_can_auto_assign_driver_when_no_available_drivers():
    owner_token = get_token("bob", "securepass")

    with patch("app.routers.delivery.auto_assign_driver",
               side_effect=HTTPException(status_code=404, detail="No available drivers found")):
        response = client.post("/delivery/orders/cust-odr-1/auto-assign-driver",
                            headers=auth_header(owner_token),
                            )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "No available drivers found"

def test_restaurant_owner_can_assign_specific_driver():
    owner_token = get_token("bob", "securepass")

    with patch("app.routers.delivery.assign_driver_to_order", return_value=FAKE_ASSIGN_RESULT):
        response = client.post("/delivery/orders/cust-odr-1/assign/1",
                            headers=auth_header(owner_token),
                            )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["order"]["assigned_driver_id"] == 1

def test_restaurant_owner_can_assign_specific_driver_when_driver_busy():
    owner_token = get_token("bob", "securepass")

    with patch("app.routers.delivery.assign_driver_to_order",
               side_effect=HTTPException(status_code=400, detail="Driver is not available")):
        response = client.post("/delivery/orders/cust-odr-1/assign/1",
                            headers=auth_header(owner_token),
                            )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Driver is not available"

def test_restaurant_owner_can_assign_specific_driver_when_order_already_assigned():
    owner_token = get_token("bob", "securepass")

    with patch("app.routers.delivery.assign_driver_to_order",
               side_effect=HTTPException(status_code=400, detail="Order already has an assigned driver")):
        response = client.post("/delivery/orders/cust-odr-1/assign/1",
                            headers=auth_header(owner_token),
                            )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Order already has an assigned driver"

def test_customer_cannot_assign_driver():
    customer_token = get_token("alice", "password123")
    response = client.post("/delivery/orders/cust-odr-1/assign/1", 
                            headers=auth_header(customer_token),
                            )
    assert response.status_code == 403