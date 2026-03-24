from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.order_notification_service import (
    notify_order_placed,
    notify_out_for_delivery,
    notify_order_delivered,
    notify_order_delayed
)

client = TestClient(app)

# helper so we dont repeat patch everywhere
def mock_notifications():
    return (
        patch("app.services.notification_service.load_all_notifications", return_value=[]),
        patch("app.services.notification_service.save_all_notifications")
    )

def get_admin_header():
    token = client.post("/auth/login", data={
        "username": "admin",
        "password": "adminpass"
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def get_customer_header():
    token = client.post("/auth/login", data={
        "username": "alice",
        "password": "password123"
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Integration Tests

def test_notify_order_placed_returns_200():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            r = client.post("/order-notifications/placed", json={
                "order_id": "1d8e87M",
                "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
                "restaurant_id": 16
            }, headers=get_admin_header())
    assert r.status_code == 200
    data = r.json()
    assert data["customer_id"] == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert data["restaurant_id"] == 16
    assert "1d8e87M" in data["message"]

def test_notify_out_for_delivery_returns_200():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            r = client.post("/order-notifications/out-for-delivery", json={
                "order_id": "1d8e87M",
                "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
                "restaurant_id": 16,
                "driver_name": "Charlie"
            }, headers=get_admin_header())
    assert r.status_code == 200
    assert "Charlie" in r.json()["message"]

def test_notify_order_delivered_returns_200():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            r = client.post("/order-notifications/delivered", json={
                "order_id": "1d8e87M",
                "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
                "restaurant_id": 16
            }, headers=get_admin_header())
    assert r.status_code == 200
    assert r.json()["status"] == "delivered"

def test_notify_order_delayed_returns_200():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            r = client.post("/order-notifications/delayed", json={
                "order_id": "1d8e87M",
                "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
                "restaurant_id": 16,
                "delay_minutes": 15.0
            }, headers=get_admin_header())
    assert r.status_code == 200
    assert "15.0" in r.json()["message"]

def test_notify_order_placed_unauthorized_returns_401():
    r = client.post("/order-notifications/placed", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16
    })
    assert r.status_code == 401

def test_notify_order_placed_wrong_role_returns_403():
    r = client.post("/order-notifications/placed", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16
    }, headers=get_customer_header())
    assert r.status_code == 403

# Validation Tests (no mocking needed - requests fail before hitting the service)

def test_notify_order_placed_missing_field_returns_422():
    r = client.post("/order-notifications/placed", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    }, headers=get_admin_header())
    assert r.status_code == 422

def test_notify_order_delayed_missing_delay_returns_422():
    r = client.post("/order-notifications/delayed", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16
    }, headers=get_admin_header())
    assert r.status_code == 422

def test_notify_order_placed_empty_body_returns_422():
    r = client.post("/order-notifications/placed", json={}, headers=get_admin_header())
    assert r.status_code == 422

# Unit Tests

def test_unit_notify_order_placed_message_content():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            result = notify_order_placed("1d8e87M", "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16)
    assert "1d8e87M" in result.message
    assert result.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"

def test_unit_notify_out_for_delivery_includes_driver():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            result = notify_out_for_delivery("1d8e87M", "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Charlie")
    assert "Charlie" in result.message

def test_unit_notify_order_delivered_status():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            result = notify_order_delivered("1d8e87M", "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16)
    assert result.status == "delivered"

def test_unit_notify_order_delayed_includes_minutes():
    with patch("app.services.notification_service.load_all_notifications", return_value=[]):
        with patch("app.services.notification_service.save_all_notifications"):
            result = notify_order_delayed("1d8e87M", "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, 15.0)
    assert "15.0" in result.message