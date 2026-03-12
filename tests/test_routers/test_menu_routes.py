from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Helper to get token using valid credentials
def get_token(username: str, password: str) -> str:
    response = client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def test_create_menu_item_as_owner_only():
    owner_token = get_token("bob", "securepass")
    response = client.post("/menu/1",
                            json={"name": "Burger", "price": 9.99},
                            headers=auth_header(owner_token)
                        )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["item"]["restaurant_id"] == 1
    assert data["item"]["name"] == "Burger"

def test_create_menu_item_forbidden_for_customer():
    customer_token = get_token("alice", "password123")
    response = client.post("/menu/1",
                            json={"name": "Fries", "price": 4.99},
                            headers=auth_header(customer_token)
                        )
    assert response.status_code == 403, response.text

def test_update_menu_item_validates_restaurant_ownership():
    owner_token = get_token("bob", "securepass")
    # First create an item for restaurant 1
    response = client.post("/menu/1",
                                  json={"name": "Grass", "price": 5.99},
                                  headers=auth_header(owner_token)
                              )
    assert response.status_code == 201, response.text
    menu_id = response.json()["item"]["id"]

    # Updating it with a different restaurant ID i.e. 2, should fail with 403
    update_response = client.put(f"/menu/2/{menu_id}",
                                 json={"name": "Salad"},
                                 headers=auth_header(owner_token)
                             )
    assert update_response.status_code == 403, update_response.text

def test_delete_menu_item_validates_restaurant_ownership():
    owner_token = get_token("bob", "securepass")
    # First create an item for restaurant 3
    response = client.post("/menu/3",
                            json={"name": "Soda", "price": 1.99},
                            headers=auth_header(owner_token)
                        )
    assert response.status_code == 201, response.text
    menu_id = response.json()["item"]["id"]

    # Wrong restaurant in path mean it fails with 403
    delete_response = client.delete(f"/menu/2/{menu_id}",
                                   headers=auth_header(owner_token)
                               )
    assert delete_response.status_code == 403, delete_response.text

    # Correct restaurant should succeed
    delete_response = client.delete(f"/menu/3/{menu_id}",
                                   headers=auth_header(owner_token)
                               )
    assert delete_response.status_code == 200, delete_response.text