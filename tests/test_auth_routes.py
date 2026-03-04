import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# helper 
def get_token(username, password):
    r = client.post("/auth/login", data={"username": username, "password": password})
    return r.json()["access_token"]

def test_valid_login_returns_token():
    r = client.post("/auth/login", data={"username": "alice", "password": "password123"})
    assert r.status_code == 200
    assert "access_token" in r.json()
    assert r.json()["token_type"] == "bearer"

def test_wrong_password_returns_401():
    r = client.post("/auth/login", data={"username": "alice", "password": "wrongpass"})
    assert r.status_code == 401

def test_nonexistent_user_returns_401():
    r = client.post("/auth/login", data={"username": "nobody", "password": "anything"})
    assert r.status_code == 401

def test_empty_username_returns_error():
    r = client.post("/auth/login", data={"username": "", "password": "password123"})
    assert r.status_code in (401, 422)


# send broken/malformed tokens and verify they are rejected

def test_fake_token_is_rejected():
    r = client.get("/auth/me", headers={"Authorization": "Bearer fake.token.value"})
    assert r.status_code == 401

def test_tampered_token_is_rejected():
    token = get_token("alice", "password123")
    tampered = token[:-5] + "XXXXX"
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {tampered}"})
    assert r.status_code == 401

def test_expired_token_is_rejected():
    from app.auth.jwt_handler import create_access_token
    expired = create_access_token({"sub": "alice", "role": "customer"}, expires_minutes=-1)
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"})
    assert r.status_code == 401

def test_missing_auth_header_is_rejected():
    r = client.get("/auth/me")
    assert r.status_code == 401


# verify right HTTP status codes come back (not just any error)

def test_wrong_role_returns_403_not_401():
    token = get_token("alice", "password123")
    r = client.get("/auth/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403

def test_error_response_has_detail_field():
    r = client.post("/auth/login", data={"username": "nobody", "password": "bad"})
    assert "detail" in r.json()

def test_401_includes_www_authenticate_header():
    r = client.get("/auth/me")
    assert "www-authenticate" in r.headers


# patch service layer to test the router

def test_router_passes_correct_args_to_service():
    mock_return = {"access_token": "mocked", "token_type": "bearer"}
    with patch("app.routers.auth.login_user", return_value=mock_return) as mock:
        client.post("/auth/login", data={"username": "alice", "password": "password123"})
        mock.assert_called_once_with("alice", "password123")

def test_router_returns_whatever_service_returns():
    mock_return = {"access_token": "test_token_abc", "token_type": "bearer"}
    with patch("app.routers.auth.login_user", return_value=mock_return):
        r = client.post("/auth/login", data={"username": "alice", "password": "password123"})
    assert r.json()["access_token"] == "test_token_abc"


# role based access

def test_admin_can_reach_admin_route():
    token = get_token("admin", "adminpass")
    r = client.get("/auth/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

def test_customer_cannot_reach_admin_route():
    token = get_token("alice", "password123")
    r = client.get("/auth/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403

def test_me_returns_correct_user_info():
    token = get_token("alice", "password123")
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["username"] == "alice"
    assert r.json()["role"] == "customer"

# testing logout route
def test_logout_returns_200():
    r = client.get("/auth/logout")
    assert r.status_code == 200
    assert r.json()["message"] == "Logout successful (client should delete token)"

def test_logout_does_not_invalidate_jwt_token():
    token = get_token("alice", "password123")
    client.get("/auth/logout")
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200