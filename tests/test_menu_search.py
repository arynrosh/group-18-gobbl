from fastapi.testclient import TestClient
from app.main import app
from app.services.menu_item_service import search_by_name

client = TestClient(app)

# Integration Tests

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

def test_search_by_name_empty_string():
    r = client.get("/menu/search/name?name=")
    assert r.status_code == 200

def test_search_by_name_partial_match():
    r = client.get("/menu/search/name?name=burg")
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0

def test_search_by_name_returns_correct_fields():
    r = client.get("/menu/search/name?name=Pasta")
    assert r.status_code == 200
    data = r.json()
    assert all("id" in item for item in data)
    assert all("name" in item for item in data)
    assert all("price" in item for item in data)
    assert all("restaurant_id" in item for item in data)

def test_search_by_name_across_multiple_restaurants():
    r = client.get("/menu/search/name?name=Pasta")
    assert r.status_code == 200
    data = r.json()
    restaurant_ids = set(item["restaurant_id"] for item in data)
    assert len(restaurant_ids) > 1

# Unit Tests

def test_unit_search_by_name_returns_results():
    result = search_by_name("Pasta")
    assert len(result) > 0
    assert all("Pasta" in item.name for item in result)

def test_unit_search_by_name_no_match():
    result = search_by_name("xyznonexistentitem")
    assert result == []

def test_unit_search_by_name_case_insensitive():
    result_lower = search_by_name("pasta")
    result_upper = search_by_name("Pasta")
    assert len(result_lower) == len(result_upper)

def test_unit_search_by_name_partial_match():
    result = search_by_name("burg")
    assert len(result) > 0

def test_unit_search_by_name_returns_correct_type():
    result = search_by_name("Pasta")
    assert isinstance(result, list)

def test_unit_search_by_name_empty_string():
    result = search_by_name("")
    assert isinstance(result, list)