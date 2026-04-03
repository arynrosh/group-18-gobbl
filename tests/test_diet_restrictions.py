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
from app.repositories.users_repo import load_all_users

client = TestClient(app)

VALID_USER_COSTUMER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password1",
    "role": "customer",
    "diet_restrictions": ["Banana Allergy"]
}

VALID_USER_OTHER = {
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "password2",
    "role": "restaurant_owner",
    #"diet_restrictions": None
}

#remove later
"""def test_valid_registration_returns_201():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_COSTUMER)
    assert r.status_code == 201
    assert r.json()["username"] == "testuser"
    """

#is saying restrictions don't exist
def test_create_diet_restrictions_true():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_COSTUMER)
    assert r.status_code == 201
    data = r.json()
    restrictions = data.get('diet_restrictions')
    assert restrictions == ["Banana Allergy"] #r.json()["diet_restrictions"] == []

def test_create_diet_restrictions_false():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_OTHER)
    assert r.status_code == 201
    data = r.json()
    restrictions = data.get('diet_restrictions')
    assert restrictions == None

def test_add_diet_restriction():
    restriction = "Nut Allergy"
    username = "alice"
    restrictions = add_diet_restriction(username, restriction)
    assert restriction in restrictions

def test_remove_diet_restriction_completed():
    restriction = "Banana Allergy"
    username = "sadie"
    restrictions = remove_diet_restriction(username, restriction)
    assert restriction not in restrictions

#pytest tests/test_diet_restrictions.py