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

#is saying diet_restrictions don't exist
def test_add_diet_restriction():
    restriction = "Nut Allergy"
    username = "alice"
    all_restrictions = load_all_diet_restrictions()
    add_diet_restriction(username, restriction)
    
    user = get_diet_restrictions_or_404(username, all_restrictions)
    assert restriction in user["diet_restrictions"]

#is saying diet_restrictions don't exist
def test_remove_diet_restriction_nonlisted_restriction():
    restriction = "Banana Allergy"
    username = "alice"
    all_restrictions = load_all_diet_restrictions()
    remove_diet_restriction(username, restriction)
    user = get_diet_restrictions_or_404(username, all_restrictions)
    assert "Banana Allergy" not in user["diet_restrictions"]

def test_remove_diet_restriction_listed_restriction():
    restriction = "Vegan"
    username = "alice"
    all_restrictions = load_all_diet_restrictions()
    remove_diet_restriction(username, restriction)
    user = get_diet_restrictions_or_404(username, all_restrictions)
    assert "Vegan" not in user["diet_restrictions"]

def test_create_diet_restrictions():
    costumer = create_diet_restrictions("customer")
    not_costumer = create_diet_restrictions("restaurant_owner")
    assert costumer == True
    assert not_costumer == False

#pytest tests/test_diet_restrictions.py