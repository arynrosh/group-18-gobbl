from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_by_name_valid():
    response = client.get("/restaurant/search/name?name=cactus")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0
    assert any("Cactus" in r["restaurant_name"] for r in data["items"])

def test_search_by_name_no_match():
    response = client.get("/restaurant/search/name?name=xyznonexistent")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []

def test_search_by_name_case_insensitive():
    response = client.get("/restaurant/search/name?name=cactus")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0

def test_search_by_cuisine_valid():
    response = client.get("/restaurant/search/cuisine?cuisine=Chinese")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0
    assert any(r["cuisine"] == "Chinese" for r in data["items"])

def test_search_by_cuisine_no_match():
    response = client.get("/restaurant/search/cuisine?cuisine=Nigerian")
    assert response.status_code == 200
    assert response.json()["items"] == []

def test_search_by_cuisine_case_insensitive():
    response = client.get("/restaurant/search/cuisine?cuisine=chinese")
    assert response.status_code == 200
    assert len(response.json()["items"]) > 0

def test_search_by_name_empty_string():
    response = client.get("/restaurant/search/name?name=")
    assert response.status_code == 200

def test_search_by_cuisine_empty_string():
    response = client.get("/restaurant/search/cuisine?cuisine=")
    assert response.status_code == 200

def test_search_by_name_partial_match():
    response = client.get("/restaurant/search/name?name=momo")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0

def test_search_by_cuisine_partial_match():
    response = client.get("/restaurant/search/cuisine?cuisine=ital")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0