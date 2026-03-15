from fastapi.testclient import TestClient
from app.services import restaurant_service
from app.main import app

client = TestClient(app)


# Helper to get token using valid credentials
def get_token(username: str, password: str) -> str:
    response = client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def reset_menu_data():
    restaurant_service.reset_menu_data()

def setup_function():
    reset_menu_data()

def test_create_menu_item_as_owner_only():
    owner_token = get_token("bob", "securepass")
    response = client.post("/menu/1",
                            json={"food_item": "Burger", "order_value": 9.99},
                            headers=auth_header(owner_token)
                        )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["item"]["restaurant_id"] == 1
    assert data["item"]["food_item"] == "Burger"
    assert data["item"]["order_value"] == 9.99

def test_create_menu_item_forbidden_for_customer():
    customer_token = get_token("alice", "password123")
    response = client.post("/menu/1",
                            json={"food_item": "Fries", "order_value": 4.99},
                            headers=auth_header(customer_token)
                        )
    assert response.status_code == 403, response.text

def test_update_menu_item_validates_restaurant_ownership():
    owner_token = get_token("bob", "securepass")
    create_response = client.post("/menu/1",
                                  json={"food_item": "Grass", "order_value": 5.99},
                                  headers=auth_header(owner_token)
                              )
    assert create_response.status_code == 201, create_response.text
    menu_id = create_response.json()["item"]["id"]

    update_response = client.put(f"/menu/2/{menu_id}",
                                 json={"food_item": "Salad", "order_value": 6.99},
                                 headers=auth_header(owner_token)
                             )
    assert update_response.status_code == 403, update_response.text

def test_delete_menu_item_validates_restaurant_ownership():
    owner_token = get_token("bob", "securepass")
    create_response = client.post("/menu/3",
                            json={"food_item": "Soda", "order_value": 1.99},
                            headers=auth_header(owner_token)
                        )
    assert create_response.status_code == 201, create_response.text
    menu_id = create_response.json()["item"]["id"]

    delete_response = client.delete(f"/menu/2/{menu_id}",
                                   headers=auth_header(owner_token)
                               )
    assert delete_response.status_code == 403, delete_response.text

    delete_response = client.delete(f"/menu/3/{menu_id}",
                                   headers=auth_header(owner_token)
                               )
    assert delete_response.status_code == 200, delete_response.text


def test_list_menu_items_without_filters():
    owner_token = get_token("bob", "securepass")
    client.post("/menu/1",
                json={"food_item": "Burger", "order_value": 9.99},
                headers=auth_header(owner_token)
    )
    client.post("/menu/1",
                json={"food_item": "Fries", "order_value": 4.99},
                headers=auth_header(owner_token)
    )
    response = client.get("/menu/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2 

def test_filter_menu_items_by_price_tier():
    owner_token = get_token("bob", "securepass")
    client.post("/menu/1",
                json={"food_item": "Burger", "order_value": 9.99},
                headers=auth_header(owner_token)
    )
    client.post("/menu/1",
                json={"food_item": "Tacos", "order_value": 42.21},
                headers=auth_header(owner_token)
    )
    response = client.get("/menu/1?price_tier=$$$$")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["food_item"] == "Tacos"


def test_filter_menu_items_by_rating():
    #references json file since schemas don't have customer_rating field (cuz restaurant owner doesn't set it when creating/updating menu item)
    response = client.get("/menu/53?min_rating=3.0")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["food_item"] == "Burger"
    assert data[0]["customer_rating"] == 3.0

def test_filter_menu_items_no_results():
    owner_token = get_token("bob", "securepass")
    client.post("/menu/1",
                json={"food_item": "Cola", "order_value": 2.99, "customer_rating": 2.0},
                headers=auth_header(owner_token)
            )
    response = client.get("/menu/1?order_value=$$&min_rating=4.0")
    assert response.status_code == 200
    data = response.json()
    assert data == []