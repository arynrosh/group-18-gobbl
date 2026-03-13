from fastapi.testclient import TestClient
from app.routers import restaurant as menu_router
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
    menu_router.menu_db.clear()
    menu_router.menu_id_counter = 1

def setup_function():
    reset_menu_data()

def test_create_menu_item_as_owner_only():
    owner_token = get_token("bob", "securepass")
    response = client.post("/menu/1",
                            json={"name": "Burger", "price": 9.99, "category": "Main", "available": True},
                            headers=auth_header(owner_token)
                        )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["item"]["restaurant_id"] == 1
    assert data["item"]["name"] == "Burger"

def test_create_menu_item_forbidden_for_customer():
    customer_token = get_token("alice", "password123")
    response = client.post("/menu/1",
                            json={"name": "Fries", "price": 4.99, "category": "Sides", "available": True},
                            headers=auth_header(customer_token)
                        )
    assert response.status_code == 403, response.text

def test_update_menu_item_validates_restaurant_ownership():
    owner_token = get_token("bob", "securepass")
    # First create an item for restaurant 1
    response = client.post("/menu/1",
                                  json={"name": "Grass", "price": 5.99, "category": "Sides", "available": True},
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
                            json={"name": "Soda", "price": 1.99, "category": "Drinks", "available": True},
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


def test_list_menu_items_without_filters():
    owner_token = get_token("bob", "securepass")
    client.post("/menu/1",
                json={"name": "Burger", "price": 9.99, "category": "Main", "available": True},
                headers=auth_header(owner_token)
    )
    client.post("/menu/1",
                json={"name": "Fries", "price": 4.99, "category": "Sides", "available": True},
                headers=auth_header(owner_token)
    )
    response = client.get("/menu/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2 

def test_filter_menu_items_by_category():
    owner_token = get_token("bob", "securepass")
    client.post("/menu/1",
                json={"name": "Cola", "price": 2.99, "category": "Drinks", "available": True},
                headers=auth_header(owner_token)
    )
    client.post("/menu/1",
                json={"name": "Burger", "price": 9.99, "category": "Main", "available": True},
                headers=auth_header(owner_token)
    )
    response = client.get("/menu/1?category=Drinks")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Cola"

def test_filter_menu_items_by_availability():
    owner_token = get_token("bob", "securepass")
    client.post("/menu/1",
                json={"name": "Burger", "price": 9.99, "category": "Main", "available": True},
                headers=auth_header(owner_token)
    )
    client.post("/menu/1",
                json={"name": "Fries", "price": 4.99, "category": "Sides", "available": False},
                headers=auth_header(owner_token)
    )
    response = client.get("/menu/1?available=True")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Burger"

def test_filter_menu_items_by_category_and_availability():
    owner_token = get_token("bob", "securepass")
    client.post("/menu/1",
                json={"name": "Cola", "price": 2.99, "category": "Drinks", "available": True},
                headers=auth_header(owner_token)
    )
    client.post("/menu/1",
                json={"name": "Orange Juice", "price": 3.99, "category": "Drinks", "available": False},
                headers=auth_header(owner_token)
    )
    client.post("/menu/1",
                json={"name": "Burger", "price": 9.99, "category": "Main", "available": True},
                headers=auth_header(owner_token)
    )
    response = client.get("/menu/1?available=True&category=Drinks")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Cola"

def test_filter_menu_items_no_results():
    owner_token = get_token("bob", "securepass")
    client.post("/menu/1",
                json={"name": "Cola", "price": 2.99, "category": "Drinks", "available": True},
                headers=auth_header(owner_token)
            )
    response = client.get("/menu/1?available=True&category=Dessert")
    assert response.status_code == 200
    data = response.json()
    assert data == []