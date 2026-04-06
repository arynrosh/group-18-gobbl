# Tests for discount code feature (Barha's Individual Feature)

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_DISCOUNT = {
    "code_id": "abc-123",
    "code": "SAVE10",
    "percentage": 10.0,
    "expiry": "2099-12-31",
    "assigned_to": ["alice"],
    "used_by": []
}

VALID_ORDER = {
    "order_id": "order-001",
    "customer_id": "alice",
    "restaurant_id": 53,
    "delivery_distance": 5,
    "assigned_driver_id": None,
    "items": [{"restaurant_id": 53, "food_item": "Burger", "quantity": 1, "order_value": 41.17}],
    "sent": True
}

def get_admin_header():
    token = client.post("/auth/login", data={"username": "admin", "password": "adminpass"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def get_auth_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def get_owner_header():
    token = client.post("/auth/login", data={"username": "bob", "password": "securepass"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# equivalence partitioning

def test_admin_can_create_discount():
    with patch("app.services.discount_service.load_all_discounts", return_value=[]):
        with patch("app.services.discount_service.save_all_discounts"):
            r = client.post("/discounts", json={
                "code": "SAVE10",
                "percentage": 10.0,
                "expiry": "2099-12-31",
                "assigned_to": ["alice"]
            }, headers=get_admin_header())
    assert r.status_code == 201
    assert r.json()["code"] == "SAVE10"

def test_customer_can_view_their_codes():
    with patch("app.services.discount_service.load_all_discounts", return_value=[VALID_DISCOUNT]):
        r = client.get("/discounts/my-codes", headers=get_auth_header())
    assert r.status_code == 200
    assert r.json()[0]["code"] == "SAVE10"

def test_payment_with_valid_discount_reduces_amount():
    with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER]):
        with patch("app.services.payment_service.load_all_payments", return_value=[]):
            with patch("app.services.payment_service.save_all_payments"):
                with patch("app.services.discount_service.load_all_discounts", return_value=[VALID_DISCOUNT]):
                    with patch("app.services.discount_service.save_all_discounts"):
                        r = client.post("/payments/process", json={
                            "order_id": "order-001",
                            "cardholder_name": "John Doe",
                            "card_number": "1234567890123456",
                            "expiry": "12/26",
                            "cvv": "123",
                            "discount_code": "SAVE10"
                        }, headers=get_auth_header())
    assert r.status_code == 200
    assert r.json()["status"] == "approved"


# fault injection

def test_expired_discount_not_returned():
    expired = {**VALID_DISCOUNT, "expiry": "2000-01-01"}
    with patch("app.services.discount_service.load_all_discounts", return_value=[expired]):
        r = client.get("/discounts/my-codes", headers=get_auth_header())
    assert len(r.json()) == 0

def test_duplicate_discount_code_returns_409():
    with patch("app.services.discount_service.load_all_discounts", return_value=[VALID_DISCOUNT]):
        r = client.post("/discounts", json={
            "code": "SAVE10",
            "percentage": 10.0,
            "expiry": "2099-12-31",
            "assigned_to": ["alice"]
        }, headers=get_admin_header())
    assert r.status_code == 409

def test_unassigned_discount_returns_403():
    other_discount = {**VALID_DISCOUNT, "assigned_to": ["bob"]}
    with patch("app.services.discount_service.load_all_discounts", return_value=[other_discount]):
        with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER]):
            with patch("app.services.payment_service.load_all_payments", return_value=[]):
                with patch("app.services.payment_service.save_all_payments"):
                    r = client.post("/payments/process", json={
                        "order_id": "order-001",
                        "cardholder_name": "John Doe",
                        "card_number": "1234567890123456",
                        "expiry": "12/26",
                        "cvv": "123",
                        "discount_code": "SAVE10"
                    }, headers=get_auth_header())
    assert r.status_code == 403


# exception handling

def test_non_admin_cannot_create_discount():
    r = client.post("/discounts", json={
        "code": "SAVE10",
        "percentage": 10.0,
        "expiry": "2099-12-31",
        "assigned_to": ["alice"]
    }, headers=get_auth_header())
    assert r.status_code == 403

def test_unauthenticated_cannot_create_discount():
    r = client.post("/discounts", json={
        "code": "SAVE10",
        "percentage": 10.0,
        "expiry": "2099-12-31",
        "assigned_to": ["alice"]
    })
    assert r.status_code == 401


# mocking

def test_create_discount_saves_to_storage():
    with patch("app.services.discount_service.load_all_discounts", return_value=[]):
        with patch("app.services.discount_service.save_all_discounts") as mock_save:
            client.post("/discounts", json={
                "code": "SAVE10",
                "percentage": 10.0,
                "expiry": "2099-12-31",
                "assigned_to": ["alice"]
            }, headers=get_admin_header())
    assert mock_save.called

def test_applying_discount_marks_code_as_used():
    with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER]):
        with patch("app.services.payment_service.load_all_payments", return_value=[]):
            with patch("app.services.payment_service.save_all_payments"):
                with patch("app.services.payment_service.validate_and_apply_discount", return_value=37.05) as mock_discount:
                    client.post("/payments/process", json={
                        "order_id": "order-001",
                        "cardholder_name": "John Doe",
                        "card_number": "1234567890123456",
                        "expiry": "12/26",
                        "cvv": "123",
                        "discount_code": "SAVE10"
                    }, headers=get_auth_header())
    assert mock_discount.called
