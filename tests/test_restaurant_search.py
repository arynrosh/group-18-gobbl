from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_by_name_valid():
    
    response = client.get("/restaurant/search/name?name=club")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any("club" in r["name"] for r in data)

def test_search_by_name_no_match():
    
    response = client.get("/restaurant/search/name?name=xyznonexistent")
    assert response.status_code == 200
    data = response.json()
    assert data == []

def test_search_by_name_case_insensitive():
    
    response = client.get("/restaurant/search/name?name=club")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_search_by_cuisine_valid():
   
    response = client.get("/restaurant/search/cuisine?cuisine=Chinese")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(r["cuisine"] == "Chinese" for r in data)

def test_search_by_cuisine_no_match():
    
    response = client.get("/restaurant/search/cuisine?cuisine=Nigerian")
    assert response.status_code == 200
    assert response.json() == []

def test_search_by_cuisine_case_insensitive():
   
    response = client.get("/restaurant/search/cuisine?cuisine=mexican")
    assert response.status_code == 200
    assert len(response.json()) > 0