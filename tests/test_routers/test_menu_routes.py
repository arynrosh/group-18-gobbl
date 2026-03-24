from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import HTTPException
from app.main import app

client = TestClient(app)


def get_token(username: str, password: str) -> str:
    response = client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

FAKE_MENU_ITEM = {
    "menu_item_id": 1,
    "restaurant_id": 53,
    "restaurant_name": "Cactus Club",
    "cuisine": "American",
    "food_item": "Burger",
    "order_value": 41.17,
    "customer_rating": None,
    "delivery_time_actual": None
}

FAKE_MENU_LIST= [
    {
        "menu_item_id": 1,
        "restaurant_id": 53,
        "restaurant_name": "Cactus Club",
        "cuisine": "American",
        "food_item": "Burger",
        "order_value": 41.17,
        "customer_rating": 4.0,
        "delivery_time_actual": 10.74
    },
    {
        "menu_item_id": 2,
        "restaurant_id": 53,
        "restaurant_name": "Cactus Club",
        "cuisine": "American",
        "food_item": "French Fries",
        "order_value": 12.56,
        "customer_rating": 4.0,
        "delivery_time_actual": 10.74
    }
]

def test_create_menu_item_as_restaurant_owner_only():
    owner_token = get_token("bob", "securepass")
    with patch("app.services.menu_service.create_menu_item", return_value=FAKE_MENU_ITEM):
        response = client.post("/menu/53",
                                json={"restaurant_name": "Cactus Club","cuisine": "American","food_item": "Burger", "order_value": 41.17},
                                headers=auth_header(owner_token)
                            )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["message"] == "Menu item created"
    assert data["item"]["restaurant_id"] == 53
    assert data["item"]["restaurant_name"] == "Cactus Club"
    assert data["item"]["cuisine"] == "American"
    assert data["item"]["food_item"] == "Burger"
    assert data["item"]["order_value"] == 41.17

def test_create_menu_item_forbidden_for_customer():
    customer_token = get_token("alice", "password123")
    response = client.post("/menu/1",
                            json={"restaurant_name": "Anatoli Soulaki", "cuisine": "Greek", "food_item": "Chicken Gyros", "order_value": 18.08},
                            headers=auth_header(customer_token)
                        )
    assert response.status_code == 403, response.text

def test_update_menu_item_returns_updated_item():
    owner_token = get_token("bob", "securepass")
    updated_item = {
        "menu_item_id": 1,
        "restaurant_id": 53,
        "restaurant_name": "Cactus Club",
        "cuisine": "American",
        "food_item": "Steak",
        "order_value": 42.67,
        "customer_rating": None,
        "delivery_time_actual": None      
    }

    with patch("app.services.menu_service.update_menu_item", return_value=updated_item):
        response = client.put("/menu/1/1",
                              json={"restaurant_name": "Cactus Club", "cuisine": "American", "food_item": "Salad", "order_value": 6.99},
                              headers=auth_header(owner_token),
                            )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Menu item updated"
    assert data["item"]["restaurant_id"] == 53
    assert data["item"]["restaurant_name"] == "Cactus Club"
    assert data["item"]["cuisine"] == "American"
    assert data["item"]["food_item"] == "Steak"
    assert data["item"]["order_value"] == 42.67

def test_update_menu_item_returns_403_when_forbidden():
    owner_token = get_token("bob", "securepass")
    with patch("app.services.menu_service.update_menu_item",
               side_effect=HTTPException(status_code=403, detail="Menu item does not belong to this restaurant")):
        response = client.put("/menu/2/1",
                            json={"restaurant_name": "Cactus Club", "cuisine": "American", "food_item": "Salad", "order_value": 6.99},
                            headers=auth_header(owner_token)
                        )
    assert response.status_code == 403, response.text
    assert response.json()["detail"] == "Menu item does not belong to this restaurant"

def test_delete_menu_item_returns_success_message():
    owner_token = get_token("bob", "securepass")
    with patch("app.services.menu_service.delete_menu_item", return_value=None):
        response = client.delete("/menu/2/1",
                            headers=auth_header(owner_token)
                        )
        
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Menu item deleted"}

def test_delete_menu_item_returns_403_when_forbidden():
    owner_token = get_token("bob", "securepass")
    with patch("app.services.menu_service.delete_menu_item",
               side_effect=HTTPException(status_code=403, detail="Menu item does not belong to this restaurant")):
        response = client.delete("/menu/2/1",
                            headers=auth_header(owner_token)
                        )
    assert response.status_code == 403, response.text
    assert response.json()["detail"] == "Menu item does not belong to this restaurant"

def test_list_menu_items_returns_items():
    with patch("app.services.menu_service.list_menu_items", return_value=FAKE_MENU_LIST):
        response = client.get("/menu/53")

    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2
    assert data[0]["restaurant_id"] == 53
    assert data[0]["restaurant_name"] == "Cactus Club"
    assert data[0]["cuisine"] == "American"

def test_list_menu_items_accepts_filter():
    filtered_items_list = [FAKE_MENU_LIST[1]]
    with patch("app.services.menu_service.list_menu_items", return_value=filtered_items_list):
        response = client.get("/menu/53?price_tier=$&min_rating=3.0")

    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["menu_item_id"] == 2
    assert data[0]["restaurant_id"] == 53
    assert data[0]["restaurant_name"] == "Cactus Club"
    assert data[0]["cuisine"] == "American"
    assert data[0]["food_item"] == "French Fries"
    assert data[0]["order_value"] == 12.56
    assert data[0]["customer_rating"] >= 3.0

def test_list_menu_items_no_results():
    with patch("app.services.menu_service.list_menu_items", return_value=[]):
        response = client.get("/menu/53?order_value=$$&min_rating=5.0")
        
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []

def test_list_menu_items_invalid_price_tier_returns_422():
    response = client.get("/menu/53?price_tier=abc")
    assert response.status_code == 422, response.text

def test_list_menu_items_invalid_min_rating_returns_422():
    response = client.get("/menu/53?min_rating=abc")
    assert response.status_code == 422, response.text