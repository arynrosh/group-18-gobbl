import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import delivery_service

client = TestClient(app)

def get_token(username: str, password: str) -> str:
    response = client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

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

def test_driver_can_update_distance():
    driver_token =  get_token("dave", "driverpass")
    response = client.put("/delivery/drivers/driver1/distance",
                            json={"driver_distance": 7.0},
                            headers=auth_header(driver_token)
                          )
    assert response.status_code == 200, response.text
    assert response.json()["driver"]["driver_distance"] == 7.0

def test_driver_can_update_status():
    driver_token = get_token("dave", "driverpass")
    response = client.put("/delivery/drivers/driver1/status",
                          json = {"status": "busy"},
                          headers=auth_header(driver_token),
                          )
    assert response.status_code == 200, response.text
    assert response.json()["driver"]["status"] == "busy"

def test_restaurant_owner_can_auto_assign_driver():
    owner_token = get_token("bob", "securepass")
    response = client.post("/delivery/deliveries/delivery1/auto-assign",
                           headers=auth_header(owner_token),
                           )
    assert response.status_code == 200, response.text
    assert response.json()["delivery"]["assigned_driver_id"] == "driver1"

def test_restaurant_owner_can_assign_specific_driver():
    owner_token = get_token("bob", "securepass")
    response = client.post("/delivery/deliveries/delivery2/assign/driver1",
                           headers=auth_header(owner_token),
    )
    assert response.status_code == 200, response.text
    assert response.json()["delivery"]["assigned_driver_id"] == "driver1"

def test_customer_cannot_assign_driver():
    customer_token = get_token("alice", "password123")
    response = client.post("/delivery/deliveries/delivery2/assign/driver1", 
                            headers=auth_header(customer_token),
    )
    assert response.status_code == 403