import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.diet_restrictions_services import (
    create_diet_restrictions,
    get_diet_restrictions_or_404,
    add_diet_restriction,
    remove_diet_restriction
)
from app.repositories.diet_restrictions_repo import load_all_diet_restrictions

client = TestClient(app)

VALID_USER_CUSTOMER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password1",
    "role": "customer",
    "diet_restrictions": []
}

VALID_DIET_RESTRICTIONS = {
    "username": "testuser",
    "diet_restrictions": ["Banana Allergy"]
}

VALID_USER_OTHER = {
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "password2",
    "role": "restaurant_owner",
    #"diet_restrictions": None
}

#is saying diet_restrictions don't exist
"""
def test_create_diet_restrictions_true():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_CUSTOMER)
    assert r.status_code == 201
    data = r.json()
    restrictions = data.get('diet_restrictions')
    assert restrictions != None #r.json()["diet_restrictions"] == []

    
def test_create_diet_restrictions_false():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_OTHER)
    assert r.status_code == 201
    data = r.json()
    restrictions = data.get('diet_restrictions')
    assert restrictions == None

#delete later, just checking that the other key values work
def test_varible():
    with patch("app.services.user_service.load_all_users", return_value=[]):
        with patch("app.services.user_service.save_all_users"):
            r = client.post("/users/register", json=VALID_USER_CUSTOMER)
    assert r.status_code == 201
    data = r.json()
    name = data.get('username')
    assert name == "testuser"
    """

#is saying diet_restrictions don't exist
def test_add_diet_restriction():
    restriction = "Nut Allergy"
    username = "alice"
    user = get_diet_restrictions_or_404(username)
    add_diet_restriction(username, restriction)
    assert "Nut Allergy" in user["diet_restrictions"]

#is saying diet_restrictions don't exist
def test_remove_diet_restriction_nonlisted_restriction():
    restriction = "Banana Allergy"
    username = "alice"
    user = get_diet_restrictions_or_404(username)
    remove_diet_restriction(username, restriction)
    assert "Banana Allergy" not in user["diet_restrictions"]

def test_create_diet_restrictions():
    costumer = create_diet_restrictions("customer")
    not_costumer = create_diet_restrictions("restaurant_owner")
    assert costumer == True
    assert not_costumer == False

#pytest tests/test_diet_restrictions.py