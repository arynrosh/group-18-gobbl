from fastapi.testclient import TestClient
from app.main import app
from app.services.menu_item_service import search_by_name

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

def test_unit_search_by_name_returns_results():
    result = search_by_name("Pasta")
    assert len(result) > 0
    assert all("Pasta" in item.name for item in result)

def test_unit_search_by_name_no_match():
    result = search_by_name("xyznonexistentitem")
    assert result == []