"""
Tests for order management (HR4 Tasks 4.2, 4.3, 4.4).
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_ORDER = {
    "order_id": "order-001",
    "customer_id": "alice",
    "restaurant_id": 53,
    "delivery_distance": 5,
    "assigned_driver_id": None,
    "items": [],
    "sent": False
}

VALID_STATUS = {"order_id": "order-001", "current": "pending", "complete": False}

def get_auth_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def get_owner_header():
    token = client.post("/auth/login", data={"username": "bob", "password": "securepass"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# equivalence partitioning

def test_create_order_returns_201():
    with patch("app.services.order_service.load_all_orders", return_value=[]):
        with patch("app.services.order_service.save_all_orders"):
            with patch("app.services.order_service.load_all_status", return_value=[]):
                with patch("app.services.order_service.save_all_status"):
                    r = client.post("/orders", params={
                        "order_id": "order-001",
                        "restaurant_id": 53,
                        "delivery_distance": 5,
                        "assigned_driver_id": 0
                    }, headers=get_auth_header())
    assert r.status_code == 201

def test_get_order_returns_correct_data():
    with patch("app.services.order_service.load_all_orders", return_value=[VALID_ORDER]):
        r = client.get("/orders/order-001", headers=get_auth_header())
    assert r.status_code == 200
    assert r.json()["order_id"] == "order-001"


# fault injection 

def test_cannot_modify_sent_order():
    sent_order = {**VALID_ORDER, "sent": True}
    with patch("app.services.order_service.load_all_orders", return_value=[sent_order]):
        with patch("app.services.order_service.get_menu_item", return_value={"order_value": 41.17}):
            r = client.post("/orders/order-001/items", params={
                "food_item": "Burger",
                "quantity": 1,
                "restaurant_id": 53
            }, headers=get_auth_header())
    assert r.status_code == 400

def test_cannot_send_empty_order():
    with patch("app.services.order_service.load_all_orders", return_value=[VALID_ORDER]):
        r = client.put("/orders/order-001/send", headers=get_auth_header())
    assert r.status_code == 400


# exception handling 

def test_unauthenticated_cannot_create_order():
    r = client.post("/orders", params={
        "order_id": "order-001",
        "restaurant_id": 53,
        "delivery_distance": 5,
        "assigned_driver_id": 0
    })
    assert r.status_code == 401

def test_non_customer_cannot_create_order():
    r = client.post("/orders", params={
        "order_id": "order-001",
        "restaurant_id": 53,
        "delivery_distance": 5,
        "assigned_driver_id": 0
    }, headers=get_owner_header())
    assert r.status_code == 403

def test_nonexistent_order_returns_404_with_detail():
    with patch("app.services.order_service.load_all_orders", return_value=[]):
        r = client.get("/orders/fake-order", headers=get_auth_header())
    assert r.status_code == 404
    assert "detail" in r.json()


#mocking

def test_create_order_saves_to_storage():
    with patch("app.services.order_service.load_all_orders", return_value=[]):
        with patch("app.services.order_service.save_all_orders") as mock_save:
            with patch("app.services.order_service.load_all_status", return_value=[]):
                with patch("app.services.order_service.save_all_status"):
                    client.post("/orders", params={
                        "order_id": "order-001",
                        "restaurant_id": 53,
                        "delivery_distance": 5,
                        "assigned_driver_id": 0
                    }, headers=get_auth_header())
    assert mock_save.called

def test_send_order_updates_status():
    order_with_items = {**VALID_ORDER, "items": [{"food_item": "Burger", "quantity": 1, "order_value": 41.17}]}
    with patch("app.services.order_service.load_all_orders", return_value=[order_with_items]):
        with patch("app.services.order_service.save_all_orders"):
            with patch("app.services.order_service.load_all_status", return_value=[VALID_STATUS]):
                with patch("app.services.order_service.save_all_status") as mock_save:
                    client.put("/orders/order-001/send", headers=get_auth_header())
    assert mock_save.called