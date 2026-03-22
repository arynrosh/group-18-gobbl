from fastapi.testclient import TestClient
from app.main import app
from app.services.pagination_service import paginate
from app.services.restaurant_service import restaurants

client = TestClient(app)

# Integration Tests

def test_browse_restaurants_default_pagination():
    r = client.get("/browse/restaurants")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data

def test_browse_restaurants_default_limit():
    r = client.get("/browse/restaurants")
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) <= 20

def test_browse_restaurants_custom_limit():
    r = client.get("/browse/restaurants?limit=5")
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) == 5

def test_browse_restaurants_custom_offset():
    r = client.get("/browse/restaurants?offset=2")
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) > 0

def test_browse_restaurants_limit_and_offset():
    r = client.get("/browse/restaurants?limit=3&offset=1")
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) == 3

def test_browse_restaurants_offset_beyond_total():
    r = client.get("/browse/restaurants?offset=10000")
    assert r.status_code == 200
    assert r.json()["items"] == []

def test_browse_restaurants_total_is_correct():
    r = client.get("/browse/restaurants")
    assert r.status_code == 200
    assert r.json()["total"] == len(restaurants)

def test_browse_restaurants_invalid_limit():
    r = client.get("/browse/restaurants?limit=0")
    assert r.status_code == 422

def test_browse_restaurants_limit_exceeds_max():
    r = client.get("/browse/restaurants?limit=101")
    assert r.status_code == 422

def test_browse_restaurants_negative_offset():
    r = client.get("/browse/restaurants?offset=-1")
    assert r.status_code == 422

# Unit Tests

def test_unit_paginate_basic():
    items = list(range(100))
    result = paginate(items, limit=10, offset=0)
    assert len(result["items"]) == 10
    assert result["total"] == 100

def test_unit_paginate_offset():
    items = list(range(100))
    result = paginate(items, limit=10, offset=10)
    assert result["items"][0] == 10

def test_unit_paginate_empty_list():
    result = paginate([], limit=10, offset=0)
    assert result["items"] == []
    assert result["total"] == 0

def test_unit_paginate_offset_beyond_total():
    items = list(range(5))
    result = paginate(items, limit=10, offset=100)
    assert result["items"] == []

def test_unit_paginate_returns_correct_metadata():
    items = list(range(50))
    result = paginate(items, limit=15, offset=5)
    assert result["limit"] == 15
    assert result["offset"] == 5
    assert result["total"] == 50