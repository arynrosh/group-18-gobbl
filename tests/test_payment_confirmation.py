# Tests for payment confirmation and record storage (Task 7.2).

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYMENT = {
    "order_id": "order-001",
    "cardholder_name": "John Doe",
    "card_number": "1234567890123456",
    "expiry": "12/26",
    "cvv": "123",
    "amount": 25.99
}

VALID_ORDER = {"order_id": "order-001", "customer_id": "alice", "sent": True}
VALID_ORDER_002 = {"order_id": "order-002", "customer_id": "alice", "sent": True}

def get_auth_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# equivalence partitioning

def test_payment_record_is_saved_after_approval():
    with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER]):
        with patch("app.services.payment_service.load_all_payments", return_value=[]):
            with patch("app.services.payment_service.save_all_payments") as mock_save:
                client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
                assert mock_save.called
                saved = mock_save.call_args[0][0]
                assert saved[0]["order_id"] == "order-001"
                assert saved[0]["status"] == "approved"

def test_payment_record_contains_timestamp():
    with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER]):
        with patch("app.services.payment_service.load_all_payments", return_value=[]):
            with patch("app.services.payment_service.save_all_payments") as mock_save:
                client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
                saved = mock_save.call_args[0][0]
                assert "timestamp" in saved[0]

def test_get_payment_by_order_returns_record():
    existing = [{"transaction_id": "txn-123", "order_id": "order-001", "amount": 25.99, "status": "approved", "timestamp": "2026-01-01"}]
    with patch("app.services.payment_service.load_all_payments", return_value=existing):
        r = client.get("/payments/order/order-001", headers=get_auth_header())
    assert r.status_code == 200
    assert r.json()["transaction_id"] == "txn-123"

def test_get_payment_by_transaction_returns_record():
    existing = [{"transaction_id": "txn-123", "order_id": "order-001", "amount": 25.99, "status": "approved", "timestamp": "2026-01-01"}]
    with patch("app.services.payment_service.load_all_payments", return_value=existing):
        r = client.get("/payments/transaction/txn-123", headers=get_auth_header())
    assert r.status_code == 200
    assert r.json()["order_id"] == "order-001"


# fault injection

def test_get_payment_for_nonexistent_order_returns_404():
    with patch("app.services.payment_service.load_all_payments", return_value=[]):
        r = client.get("/payments/order/nonexistent", headers=get_auth_header())
    assert r.status_code == 404

def test_get_payment_for_nonexistent_transaction_returns_404():
    with patch("app.services.payment_service.load_all_payments", return_value=[]):
        r = client.get("/payments/transaction/fake-txn", headers=get_auth_header())
    assert r.status_code == 404


# exception handling

def test_unauthenticated_cannot_view_payment():
    r = client.get("/payments/order/order-001")
    assert r.status_code == 401

def test_error_response_has_detail_field():
    with patch("app.services.payment_service.load_all_payments", return_value=[]):
        r = client.get("/payments/order/nonexistent", headers=get_auth_header())
    assert "detail" in r.json()


# mocking

def test_save_not_called_when_card_invalid():
    with patch("app.services.payment_service.save_all_payments") as mock_save:
        client.post("/payments/process", json={**VALID_PAYMENT, "cvv": "12"}, headers=get_auth_header())
        mock_save.assert_not_called()

def test_multiple_payments_accumulate_in_storage():
    with patch("app.services.payment_service.load_all_orders", return_value=[VALID_ORDER, VALID_ORDER_002]):
        with patch("app.services.payment_service.load_all_payments", return_value=[]):
            with patch("app.services.payment_service.save_all_payments") as mock_save:
                client.post("/payments/process", json=VALID_PAYMENT, headers=get_auth_header())
                client.post("/payments/process", json={**VALID_PAYMENT, "order_id": "order-002"}, headers=get_auth_header())
                assert mock_save.call_count == 2