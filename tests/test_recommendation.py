from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.recommendation_service import get_recommendations
from app.schemas.recommendation import RecommendedItem

client = TestClient(app)

MOCK_MENU = [
    {"menu_item_id": 1, "food_item": "Sushi", "cuisine": "Japanese", "restaurant_id": 54, "restaurant_name": "Momo Sushi", "order_value": 8.53, "customer_rating": 5.0},
    {"menu_item_id": 2, "food_item": "California Roll", "cuisine": "Japanese", "restaurant_id": 54, "restaurant_name": "Momo Sushi", "order_value": 14.76, "customer_rating": 4.0},
    {"menu_item_id": 3, "food_item": "Burger", "cuisine": "American", "restaurant_id": 53, "restaurant_name": "Cactus Club", "order_value": 41.17, "customer_rating": None},
]

MOCK_ORDERS = [
    {
        "order_id": "cust-odr-1",
        "customer_id": "alice",
        "restaurant_id": 54,
        "delivery_distance": 5.0,
        "assigned_driver_id": None,
        "items": [{"menu_item_id": 1, "food_item": "Sushi", "quantity": 1, "order_value": 8.53}],
        "sent": False
    }
]

def get_customer_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def get_admin_header():
    token = client.post("/auth/login", data={"username": "admin", "password": "adminpass"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── Unit tests ─────────────────────────────────────────────────────────────

def test_unit_no_order_history_returns_empty():
    with patch("app.services.recommendation_service.load_all_orders", return_value=[]), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        assert get_recommendations("alice") == []

def test_unit_excludes_already_ordered_items():
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        result = get_recommendations("alice")
    assert "Sushi" not in [r.food_item for r in result]

def test_unit_only_matching_cuisine():
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        result = get_recommendations("alice")
    assert all(r.cuisine == "Japanese" for r in result)

def test_unit_ranked_by_rating():
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        result = get_recommendations("alice")
    ratings = [r.customer_rating for r in result if r.customer_rating is not None]
    assert ratings == sorted(ratings, reverse=True)

def test_unit_limit_respected():
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        assert len(get_recommendations("alice", limit=1)) <= 1

def test_unit_returns_recommendeditem_objects():
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        result = get_recommendations("alice")
    assert all(isinstance(r, RecommendedItem) for r in result)


# ── Route tests ────────────────────────────────────────────────────────────

def test_route_valid_returns_200():
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        response = client.get("/recommendations/alice", headers=get_customer_header())
    assert response.status_code == 200

def test_route_no_history_returns_404():
    with patch("app.services.recommendation_service.load_all_orders", return_value=[]), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        response = client.get("/recommendations/alice", headers=get_customer_header())
    assert response.status_code == 404

def test_route_unauthorized_returns_401():
    response = client.get("/recommendations/alice")
    assert response.status_code == 401

def test_route_wrong_role_returns_403():
    token = client.post("/auth/login", data={"username": "bob", "password": "securepass"}).json()["access_token"]
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        response = client.get("/recommendations/alice", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_route_admin_can_access():
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        response = client.get("/recommendations/alice", headers=get_admin_header())
    assert response.status_code == 200

def test_route_response_has_expected_fields():
    with patch("app.services.recommendation_service.load_all_orders", return_value=MOCK_ORDERS), \
         patch("app.services.recommendation_service.load_all_menu_items", return_value=MOCK_MENU):
        response = client.get("/recommendations/alice", headers=get_customer_header())
    item = response.json()[0]
    assert all(k in item for k in ["menu_item_id", "food_item", "cuisine", "restaurant_id", "restaurant_name", "order_value"])