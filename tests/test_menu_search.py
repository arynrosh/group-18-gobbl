from fastapi.testclient import TestClient
from app.main import app
from app.routers.restaurant import menu_db, menu_id_counter

client = TestClient(app)

def setup_function():
    # Clear and populate menu_db before each test
    menu_db.clear()
    menu_db[1] = {"id": 1, "name": "Burger", "price": 9.99, "restaurant_id": 1}
    menu_db[2] = {"id": 2, "name": "Veggie Burger", "price": 8.99, "restaurant_id": 1}
    menu_db[3] = {"id": 3, "name": "Pizza", "price": 12.99, "restaurant_id": 2}

def test_search_by_name_valid():
    # Test that searching by a valid name returns matching menu items
    response = client.get("/menu/search/name?name=Burger")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any("Burger" in item["name"] for item in data)

def test_search_by_name_no_match():
    # Test that searching by a name with no matches returns an empty list
    response = client.get("/menu/search/name?name=Sushi")
    assert response.status_code == 200
    assert response.json() == []

def test_search_by_name_case_insensitive():
    # Test that name search is case insensitive
    response = client.get("/menu/search/name?name=burger")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_search_by_price_range_valid():
    # Test that searching by a valid price range returns matching menu items
    response = client.get("/menu/search/price?min_price=8.00&max_price=10.00")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(8.00 <= item["price"] <= 10.00 for item in data)

def test_search_by_price_range_no_match():
    # Test that searching by a price range with no matches returns an empty list
    response = client.get("/menu/search/price?min_price=50.00&max_price=100.00")
    assert response.status_code == 200
    assert response.json() == []

def test_search_by_price_range_exact_boundary():
    # Test that items at exact min and max price boundaries are included
    response = client.get("/menu/search/price?min_price=9.99&max_price=9.99")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Burger"
# Unit tests - testing service functions directly without HTTP
from app.services.menu_item_service import search_by_name, search_by_price_range

def test_unit_search_by_name_returns_correct_items():
    # Test service function directly returns correct MenuItem objects
    menu_db.clear()
    menu_db[1] = {"id": 1, "name": "Burger", "price": 9.99, "restaurant_id": 1}
    menu_db[2] = {"id": 2, "name": "Pizza", "price": 12.99, "restaurant_id": 2}

    result = search_by_name("Burger")
    assert len(result) == 1
    assert result[0].name == "Burger"
    assert result[0].price == 9.99
    assert result[0].restaurant_id == 1

def test_unit_search_by_name_empty_db():
    # Test service function returns empty list when db is empty
    menu_db.clear()
    result = search_by_name("Burger")
    assert result == []

def test_unit_search_by_price_range_returns_correct_items():
    # Test service function directly returns items within price range
    menu_db.clear()
    menu_db[1] = {"id": 1, "name": "Burger", "price": 9.99, "restaurant_id": 1}
    menu_db[2] = {"id": 2, "name": "Pizza", "price": 12.99, "restaurant_id": 2}

    result = search_by_price_range(8.00, 10.00)
    assert len(result) == 1
    assert result[0].name == "Burger"