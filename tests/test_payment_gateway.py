# Tests for simulated payment gateway endpoint (Task 7.1)

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYMENT = {
    "order_id": "order-001",
    "cardholder_name": "John Doe",
    "card_number": "1234567890123456",
    "expiry": "12/26",
    "cvv": "123"
}

VALID_ORDER = {
    "order_id": "order-001",
    "customer_id": "alice",
    "delivery_distance": 5,
    "assigned_driver_id": None,
    "items": [{"restaurant_id": 53, "food_item": "Burger", "quantity": 1, "order_value": 41.17}],
    "sent": True
}

def get_auth_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# equivalence partitioning

def test_valid_payment_is_approved():
    with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER]):
        with patch("app.services.payment_service.load_all_payments", return_value=[]):
            with patch("app.services.payment_service.save_all_payments"):
                r = client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
    assert r.status_code == 200
    assert r.json()["status"] == "approved"

def test_short_card_number_returns_400():
    r = client.post("/payments/process", json={**VALID_PAYMENT, "card_number": "12345"}, headers=get_auth_header())
    assert r.status_code == 400

def test_invalid_cvv_returns_400():
    r = client.post("/payments/process", json={**VALID_PAYMENT, "cvv": "12"}, headers=get_auth_header())
    assert r.status_code == 400

def test_negative_amount_returns_400():
    # amount is now calculated server side - test that an order with no items returns 400
    empty_order = {**VALID_ORDER, "items": []}
    with patch("app.services.payment_service.load_all_orders", return_value=[empty_order]):
        r = client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
    assert r.status_code == 400


# fault injection

def test_expired_card_returns_400():
    r = client.post("/payments/process", json={**VALID_PAYMENT, "expiry": "01/20"}, headers=get_auth_header())
    assert r.status_code == 400

def test_invalid_expiry_format_returns_400():
    r = client.post("/payments/process", json={**VALID_PAYMENT, "expiry": "1226"}, headers=get_auth_header())
    assert r.status_code == 400

def test_nonexistent_order_returns_404():
    with patch("app.services.payment_service.load_all_orders", return_value=[]):
        r = client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
    assert r.status_code == 404


# exception handling

def test_missing_fields_returns_422():
    r = client.post("/payments/process", json={"order_id": "order-001"}, headers=get_auth_header())
    assert r.status_code == 422

def test_unauthenticated_request_returns_401():
    r = client.post("/payments/process", json=VALID_PAYMENT)
    assert r.status_code == 401


# mocking

def test_approved_response_has_transaction_id():
    with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER]):
        with patch("app.services.payment_service.load_all_payments", return_value=[]):
            with patch("app.services.payment_service.save_all_payments"):
                with patch("app.services.payment_service.uuid.uuid4", return_value="test-uuid"):
                    r = client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
    assert r.json()["transaction_id"] == "test-uuid"

def test_unique_transaction_ids_generated():
    with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER]):
        with patch("app.services.payment_service.load_all_payments", return_value=[]):
            with patch("app.services.payment_service.save_all_payments"):
                r1 = client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
                r2 = client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
    assert r1.json()["transaction_id"] != r2.json()["transaction_id"]