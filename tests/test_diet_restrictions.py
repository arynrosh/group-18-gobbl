import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.user_service import (
    create_diet_restrictions,
    get_diet_restrictions_or_404,
    add_diet_restriction,
    remove_diet_restriction
)

client = TestClient(app)

VALID_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password1",
    "role": "customer"
}
def test_create_diet_restrictions_true():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER)
    assert r.r.json()["diet_restriction"] == []

#pytest tests/test_diet_restrictions.py