
#Tests for order fulfillment gate (Task 7.4).


from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

APPROVED_PAYMENT = [{"order_id": "order-001", "status": "approved", "transaction_id": "txn-123", "amount": 25.99, "timestamp": "2026-01-01"}]
REJECTED_PAYMENT = [{"order_id": "order-001", "status": "rejected", "transaction_id": "txn-456", "amount": 25.99, "timestamp": "2026-01-01"}]

def get_auth_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# equivalence partitioning 

def test_order_with_approved_payment_can_be_fulfilled():
    with patch("app.services.fulfillment_service.load_all_payments", return_value=APPROVED_PAYMENT):
        with patch("app.services.fulfillment_service.load_all_orders", return_value=[]):
            with patch("app.services.fulfillment_service.save_all_orders"):
                r = client.post("/orders/order-001/fulfill", headers=get_auth_header())
    assert r.status_code == 200
    assert r.json()["fulfillment_status"] == "fulfilled"

def test_order_without_payment_returns_402():
    with patch("app.services.fulfillment_service.load_all_payments", return_value=[]):
        r = client.post("/orders/order-001/fulfill", headers=get_auth_header())
    assert r.status_code == 402

def test_fulfillment_status_returns_pending_when_no_record():
    with patch("app.services.fulfillment_service.load_all_orders", return_value=[]):
        r = client.get("/orders/order-001/fulfillment-status", headers=get_auth_header())
    assert r.json()["fulfillment_status"] == "pending"


# fault injection 

def test_order_with_rejected_payment_returns_402():
    with patch("app.services.fulfillment_service.load_all_payments", return_value=REJECTED_PAYMENT):
        r = client.post("/orders/order-001/fulfill", headers=get_auth_header())
    assert r.status_code == 402

def test_already_fulfilled_order_returns_400():
    existing = [{"order_id": "order-001", "fulfillment_status": "fulfilled"}]
    with patch("app.services.fulfillment_service.load_all_payments", return_value=APPROVED_PAYMENT):
        with patch("app.services.fulfillment_service.load_all_orders", return_value=existing):
            r = client.post("/orders/order-001/fulfill", headers=get_auth_header())
    assert r.status_code == 400


# exception handling 

def test_unauthenticated_cannot_fulfill_order():
    r = client.post("/orders/order-001/fulfill")
    assert r.status_code == 401

def test_error_response_has_detail_field():
    with patch("app.services.fulfillment_service.load_all_payments", return_value=[]):
        r = client.post("/orders/order-001/fulfill", headers=get_auth_header())
    assert "detail" in r.json()


# mocking

def test_fulfill_saves_order_record():
    with patch("app.services.fulfillment_service.load_all_payments", return_value=APPROVED_PAYMENT):
        with patch("app.services.fulfillment_service.load_all_orders", return_value=[]):
            with patch("app.services.fulfillment_service.save_all_orders") as mock_save:
                client.post("/orders/order-001/fulfill", headers=get_auth_header())
                saved = mock_save.call_args[0][0]
                assert saved[0]["fulfillment_status"] == "fulfilled"

def test_fulfill_does_not_save_when_payment_missing():
    with patch("app.services.fulfillment_service.load_all_payments", return_value=[]):
        with patch("app.services.fulfillment_service.save_all_orders") as mock_save:
            client.post("/orders/order-001/fulfill", headers=get_auth_header())
            mock_save.assert_not_called()