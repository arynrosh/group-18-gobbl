import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.user_service import (
    create_diet_restrictions,
    get_user_with_diet_restrictions_or_404,
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
    "diet_restrictions": []
}

VALID_USER_OTHER = {
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "password2",
    "role": "restaurant_owner",
    #"diet_restrictions": None
}

#is saying diet_restrictions don't exist
def test_create_diet_restrictions_true():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_COSTUMER)
    assert r.status_code == 201
    data = r.json()
    restrictions = data.get('diet_restrictions')
    assert restrictions == [] #r.json()["diet_restrictions"] == []

def test_create_diet_restrictions_false():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_OTHER)
    assert r.status_code == 201
    data = r.json()
    restrictions = data.get('diet_restrictions')
    assert restrictions == None

#delete later
def test_varible():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_COSTUMER)
    assert r.status_code == 201
    data = r.json()
    name = data.get('username')
    assert name == "testuser"

#is saying diet_restrictions don't exist
def test_add_diet_restriction():
    restriction = "Nut Allergy"
    username = "alice"
    add_diet_restriction(username, restriction)
    assert restriction in username["diet_restriction"]

#is saying diet_restrictions don't exist
def test_remove_diet_restriction_completed():
    restriction = "Banana Allergy"
    username = "alice"
    restrictions = remove_diet_restriction(username, restriction)
    assert restriction not in restrictions

def test_create_diet_restrictions():
    costumer = create_diet_restrictions("costumer")
    not_costumer = create_diet_restrictions("restaurant_owner")
    assert costumer == True
    assert not_costumer == False

#pytest tests/test_diet_restrictions.py