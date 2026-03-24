from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.notification_service import send_notification, get_notifications_for_customer, get_notifications_for_restaurant
import tempfile
import json
from pathlib import Path

client = TestClient(app)

def get_admin_header():
    token = client.post("/auth/login", data={"username": "admin", "password": "adminpass"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def get_customer_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def get_restaurant_header():
    token = client.post("/auth/login", data={"username": "bob", "password": "securepass"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Integration Tests

def test_send_notification_returns_200():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            response = client.post("/notifications/send", json={
                "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
                "restaurant_id": 16,
                "message": "Your order has been placed."
            }, headers=get_admin_header())
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert data["restaurant_id"] == 16
    assert data["status"] == "delivered"

def test_send_notification_missing_field_returns_422():
    response = client.post("/notifications/send", json={
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "message": "Your order has been placed."
    }, headers=get_admin_header())
    assert response.status_code == 422

def test_send_notification_unauthorized_returns_401():
    response = client.post("/notifications/send", json={
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "message": "Your order has been placed."
    })
    assert response.status_code == 401

def test_send_notification_wrong_role_returns_403():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            response = client.post("/notifications/send", json={
                "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
                "restaurant_id": 16,
                "message": "Your order has been placed."
            }, headers=get_customer_header())
    assert response.status_code == 403

def test_get_customer_notifications_returns_200():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        response = client.get("/notifications/customer/9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
                              headers=get_customer_header())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_customer_notifications_unauthorized_returns_401():
    response = client.get("/notifications/customer/9c6dbfcb-72c5-4cc4-9f76-29200f0efda7")
    assert response.status_code == 401

def test_get_restaurant_notifications_returns_200():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        response = client.get("/notifications/restaurant/16", headers=get_restaurant_header())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_restaurant_notifications_unauthorized_returns_401():
    response = client.get("/notifications/restaurant/16")
    assert response.status_code == 401

def test_router_passes_correct_args_to_service():
    with patch("app.routers.notification.send_notification") as mock:
        mock.return_value = {
            "notification_id": 1,
            "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
            "restaurant_id": 16,
            "message": "Your order has been placed.",
            "status": "delivered",
            "timestamp": "2026-03-11T10:00:00"
        }
        client.post("/notifications/send", json={
            "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
            "restaurant_id": 16,
            "message": "Your order has been placed."
        }, headers=get_admin_header())
        mock.assert_called_once_with(
            "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Your order has been placed."
        )

# Unit Tests

def test_unit_send_notification_returns_notification():
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump([], f)
        tmp_path = Path(f.name)
    result = send_notification("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Your order has been placed.", override=tmp_path)
    assert result.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert result.restaurant_id == 16
    assert result.status == "delivered"
    tmp_path.unlink()

def test_unit_get_notifications_for_customer_returns_list():
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump([], f)
        tmp_path = Path(f.name)
    send_notification("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Your order has been placed.", override=tmp_path)
    result = get_notifications_for_customer("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", override=tmp_path)
    assert len(result) > 0
    assert all(n.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7" for n in result)
    tmp_path.unlink()

def test_unit_get_notifications_for_restaurant_returns_list():
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump([], f)
        tmp_path = Path(f.name)
    send_notification("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Your order has been placed.", override=tmp_path)
    result = get_notifications_for_restaurant(16, override=tmp_path)
    assert len(result) > 0
    assert all(n.restaurant_id == 16 for n in result)
    tmp_path.unlink()