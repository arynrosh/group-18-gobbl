# tests for user registration endpoint (Task 1.2)
# does equivalence partitioning, fault injection, exception handling, mocking

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password1",
    "role": "customer"
}

# equivalence partitioning

def test_valid_registration_returns_201():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER)
    assert r.status_code == 201
    assert r.json()["username"] == "testuser"

def test_response_does_not_include_password():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER)
    assert "password" not in r.json()

def test_all_four_roles_are_accepted():
    for role in ["customer", "restaurant_owner", "driver", "admin"]:
        with patch("app.services.user_service.load_all_users", return_value=[]):
            with patch("app.services.user_service.save_all_users"):
                r = client.post("/users/register", json={**VALID_USER, "role": role})
        assert r.status_code == 201

def test_short_username_returns_400():
    r = client.post("/users/register", json={**VALID_USER, "username": "ab"})
    assert r.status_code == 400

def test_invalid_email_returns_400():
    r = client.post("/users/register", json={**VALID_USER, "email": "notanemail"})
    assert r.status_code == 400

def test_short_password_returns_400():
    r = client.post("/users/register", json={**VALID_USER, "password": "abc123"})
    assert r.status_code == 400

def test_password_without_number_returns_400():
    r = client.post("/users/register", json={**VALID_USER, "password": "passwordonly"})
    assert r.status_code == 400

def test_invalid_role_returns_400():
    r = client.post("/users/register", json={**VALID_USER, "role": "superadmin"})
    assert r.status_code == 400


# fault injection 

def test_duplicate_username_returns_409():
    existing = [{"username": "testuser", "email": "other@example.com", "password": "pass1234", "role": "customer"}]
    with patch("app.services.user_service.load_all_users", return_value=existing):
        r = client.post("/users/register", json=VALID_USER)
    assert r.status_code == 409

def test_duplicate_email_returns_409():
    existing = [{"username": "otheruser", "email": "test@example.com", "password": "pass1234", "role": "customer"}]
    with patch("app.services.user_service.load_all_users", return_value=existing):
        r = client.post("/users/register", json=VALID_USER)
    assert r.status_code == 409


# exception handling

def test_missing_field_returns_422():
    r = client.post("/users/register", json={"username": "testuser"})
    assert r.status_code == 422

def test_error_response_has_detail_field():
    r = client.post("/users/register", json={**VALID_USER, "username": "ab"})
    assert "detail" in r.json()


# mocking

def test_register_calls_save_after_validation_passes():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users") as mock_save:
            client.post("/users/register", json=VALID_USER)
            assert mock_save.called

def test_save_not_called_on_validation_failure():
    with patch("app.services.user_service.save_all_users") as mock_save:
        client.post("/users/register", json={**VALID_USER, "username": "ab"})
        mock_save.assert_not_called()