

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MOCK_ORDERS = [
    {"restaurant_id": "16", "delivery_delay": "10.0"},
    {"restaurant_id": "16", "delivery_delay": "20.0"},
    {"restaurant_id": "30", "delivery_delay": "15.0"},
]

def get_admin_token():
    r = client.post("/auth/login", data={"username": "admin", "password": "adminpass"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def get_customer_token():
    r = client.post("/auth/login", data={"username": "alice", "password": "password123"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def get_driver_token():
    r = client.post("/auth/login", data={"username": "dave", "password": "driverpass"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# equivalence partitioning

def test_admin_can_access_delivery_times():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert r.status_code == 200

def test_admin_gets_correct_response_structure():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert "per_restaurant" in r.json()
    assert "system_wide_average_minutes" in r.json()


# fault injection

def test_customer_cannot_access_delivery_times():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=get_customer_token())
    assert r.status_code == 403

def test_driver_cannot_access_delivery_times():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=get_driver_token())
    assert r.status_code == 403


# exception handling

def test_unauthenticated_cannot_access_delivery_times():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times")
    assert r.status_code == 401

def test_invalid_token_cannot_access_delivery_times():
    headers = {"Authorization": "Bearer invalidtoken123"}
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=headers)
    assert r.status_code == 401


# mocking

def test_service_called_for_admin():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS) as mock_load:
        client.get("/statistics/delivery-times", headers=get_admin_token())
        assert mock_load.called

def test_service_not_called_for_unauthorized_user():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS) as mock_load:
        client.get("/statistics/delivery-times", headers=get_customer_token())
        mock_load.assert_not_called()