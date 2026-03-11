from fastapi.testclient import TestClient
from app.main import app
from app.services.menu_item_service import search_by_name, search_by_price_range

client = TestClient(app)



def test_search_by_name_valid():
    
    r = client.get("/menu/search/name?name=Pasta")
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    assert any("Pasta" in item["name"] for item in data)

def test_search_by_name_case_insensitive():
    
    r = client.get("/menu/search/name?name=pasta")
    assert r.status_code == 200
    assert len(r.json()) > 0

def test_search_by_name_no_match():
   
    r = client.get("/menu/search/name?name=xyznonexistentitem")
    assert r.status_code == 200
    assert r.json() == []

def test_search_by_price_range_valid():
    
    r = client.get("/menu/search/price?min_price=5.00&max_price=20.00")
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    assert all(5.00 <= item["price"] <= 20.00 for item in data)

def test_search_by_price_range_no_match():
   
    r = client.get("/menu/search/price?min_price=99999&max_price=999999")
    assert r.status_code == 200
    assert r.json() == []


def test_unit_search_by_name_returns_results():
    
    result = search_by_name("Pasta")
    assert len(result) > 0
    assert all("Pasta" in item.name for item in result)

def test_unit_search_by_name_no_match():

    result = search_by_name("xyznonexistentitem")
    assert result == []

def test_unit_search_by_price_range_returns_results():
    
    result = search_by_price_range(5.00, 20.00)
    assert len(result) > 0
    assert all(5.00 <= item.price <= 20.00 for item in result)