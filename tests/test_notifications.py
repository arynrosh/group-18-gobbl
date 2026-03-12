from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.notification_service import send_notification, get_notifications_for_customer, get_notifications_for_restaurant

client = TestClient(app)

# Integration Tests 

def test_send_notification_returns_200():
    response = client.post("/notifications/send", json={
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "message": "Your order has been placed."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert data["restaurant_id"] == 16
    assert data["status"] == "delivered"

def test_send_notification_missing_field_returns_422():
    response = client.post("/notifications/send", json={
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "message": "Your order has been placed."
    })
    assert response.status_code == 422

def test_get_customer_notifications_returns_200():
    response = client.get("/notifications/customer/9c6dbfcb-72c5-4cc4-9f76-29200f0efda7")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_restaurant_notifications_returns_200():
    response = client.get("/notifications/restaurant/16")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

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
        })
        mock.assert_called_once_with("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Your order has been placed.")

#  Unit Tests

def test_unit_send_notification_returns_notification():
    result = send_notification("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Your order has been placed.")
    assert result.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert result.restaurant_id == 16
    assert result.status == "delivered"

def test_unit_get_notifications_for_customer_returns_list():
    send_notification("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Your order has been placed.")
    result = get_notifications_for_customer("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7")
    assert len(result) > 0
    assert all(n.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7" for n in result)

def test_unit_get_notifications_for_restaurant_returns_list():
    send_notification("9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Your order has been placed.")
    result = get_notifications_for_restaurant(16)
    assert len(result) > 0
    assert all(n.restaurant_id == 16 for n in result)