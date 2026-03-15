from fastapi.testclient import TestClient
from app.main import app
from app.services.order_notification_service import (
    notify_order_placed,
    notify_out_for_delivery,
    notify_order_delivered,
    notify_order_delayed
)

client = TestClient(app)



def test_notify_order_placed_returns_200():
    response = client.post("/order-notifications/placed", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16
    })
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert data["restaurant_id"] == 16
    assert "1d8e87M" in data["message"]

def test_notify_out_for_delivery_returns_200():
    response = client.post("/order-notifications/out-for-delivery", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "driver_name": "Charlie"
    })
    assert response.status_code == 200
    data = response.json()
    assert "Charlie" in data["message"]
    assert "1d8e87M" in data["message"]

def test_notify_order_delivered_returns_200():
    response = client.post("/order-notifications/delivered", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "delivered"
    assert "1d8e87M" in data["message"]

def test_notify_order_delayed_returns_200():
    response = client.post("/order-notifications/delayed", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "delay_minutes": 15.0
    })
    assert response.status_code == 200
    data = response.json()
    assert "15.0" in data["message"]
    assert "1d8e87M" in data["message"]

def test_notify_order_placed_missing_field_returns_422():
    response = client.post("/order-notifications/placed", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    })
    assert response.status_code == 422

def test_notify_order_delayed_missing_delay_returns_422():
    response = client.post("/order-notifications/delayed", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16
    })
    assert response.status_code == 422



def test_unit_notify_order_placed():
    result = notify_order_placed("1d8e87M", "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16)
    assert result.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert result.restaurant_id == 16
    assert "1d8e87M" in result.message

def test_unit_notify_out_for_delivery():
    result = notify_out_for_delivery("1d8e87M", "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, "Charlie")
    assert result.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert "Charlie" in result.message
    assert "1d8e87M" in result.message

def test_unit_notify_order_delivered():
    result = notify_order_delivered("1d8e87M", "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16)
    assert result.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert result.status == "delivered"
    assert "1d8e87M" in result.message

def test_unit_notify_order_delayed():
    result = notify_order_delayed("1d8e87M", "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7", 16, 15.0)
    assert result.customer_id == "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7"
    assert "15.0" in result.message
    assert "1d8e87M" in result.message