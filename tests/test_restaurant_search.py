from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_by_name_valid():
    #Test that searching by a valid name returns matching restaurants.
    response = client.get("/restaurant/search/name?name=Burger")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any("Burger" in r["name"] for r in data)

def test_search_by_name_no_match():
    #Test that searching by a name with no matches returns an empty list.
    response = client.get("/restaurant/search/name?name=Pizza")
    assert response.status_code == 200
    data = response.json()
    assert data == []

def test_search_by_name_case_insensitive():
    # Test that name search is case insensitive
    response = client.get("/restaurant/search/name?name=burger")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_search_by_cuisine_valid():
    #Test that searching by a valid cuisine returns matching restaurants.
    response = client.get("/restaurant/search/cuisine?cuisine=Mexican")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(r["cuisine"] == "Mexican" for r in data)

def test_search_by_cuisine_no_match():
    #Test that searching by a cuisine with no matches returns an empty list.
    response = client.get("/restaurant/search/cuisine?cuisine=French")
    assert response.status_code == 200
    assert response.json() == []

def test_search_by_cuisine_case_insensitive():
    #Test that cuisine search is case insensitive
    response = client.get("/restaurant/search/cuisine?cuisine=mexican")
    assert response.status_code == 200
    assert len(response.json()) > 0