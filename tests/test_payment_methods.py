"""
Tests for saved payment methods (Task 7.3).
Techniques: equivalence partitioning, fault injection,
exception handling, mocking
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_METHOD = {
    "cardholder_name": "John Doe",
    "card_number": "1234567890123456",
    "expiry": "12/26"
}

def get_auth_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# equivalence partitioning

def test_save_valid_card_returns_201_with_masked_number():
    with patch("app.services.payment_methods_service.load_all_payment_methods", return_value=[]):
        with patch("app.services.payment_methods_service.save_all_payment_methods"):
            r = client.post("/payment-methods", json=VALID_METHOD, headers=get_auth_header())
    assert r.status_code == 201
    assert r.json()["last_four"] == "3456"
    assert "card_number" not in r.json()

def test_get_methods_returns_only_current_users_cards():
    existing = [
        {"method_id": "m1", "username": "alice", "cardholder_name": "Alice", "last_four": "1111", "expiry": "12/26"},
        {"method_id": "m2", "username": "bob", "cardholder_name": "Bob", "last_four": "2222", "expiry": "12/26"},
    ]
    with patch("app.services.payment_methods_service.load_all_payment_methods", return_value=existing):
        r = client.get("/payment-methods", headers=get_auth_header())
    assert len(r.json()) == 1
    assert r.json()[0]["last_four"] == "1111"


# fault injection

def test_save_invalid_card_number_returns_400():
    r = client.post("/payment-methods", json={**VALID_METHOD, "card_number": "12345"}, headers=get_auth_header())
    assert r.status_code == 400

def test_delete_another_users_card_returns_403():
    existing = [{"method_id": "m1", "username": "bob", "cardholder_name": "Bob", "last_four": "1111", "expiry": "12/26"}]
    with patch("app.services.payment_methods_service.load_all_payment_methods", return_value=existing):
        r = client.delete("/payment-methods/m1", headers=get_auth_header())
    assert r.status_code == 403


# exception handling

def test_delete_nonexistent_card_returns_404():
    with patch("app.services.payment_methods_service.load_all_payment_methods", return_value=[]):
        r = client.delete("/payment-methods/fake-id", headers=get_auth_header())
    assert r.status_code == 404

def test_unauthenticated_cannot_save_or_get_cards():
    assert client.post("/payment-methods", json=VALID_METHOD).status_code == 401
    assert client.get("/payment-methods").status_code == 401


# mocking 

def test_delete_calls_save_with_card_removed():
    existing = [{"method_id": "m1", "username": "alice", "cardholder_name": "Alice", "last_four": "3456", "expiry": "12/26"}]
    with patch("app.services.payment_methods_service.load_all_payment_methods", return_value=existing):
        with patch("app.services.payment_methods_service.save_all_payment_methods") as mock_save:
            client.delete("/payment-methods/m1", headers=get_auth_header())
            assert mock_save.call_args[0][0] == []