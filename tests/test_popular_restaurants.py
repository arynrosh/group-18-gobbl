from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.popular_restaurants_service import (
    get_popular_restaurants_by_orders,
    get_popular_restaurants_by_rating
)

client = TestClient(app)

MOCK_ORDERS = [
    {"restaurant_id": "16", "delivery_delay": "10.0"},
    {"restaurant_id": "16", "delivery_delay": "20.0"},
    {"restaurant_id": "30", "delivery_delay": "15.0"},
    {"restaurant_id": "30", "delivery_delay": "5.0"},
    {"restaurant_id": "30", "delivery_delay": "8.0"},
]

MOCK_REVIEWS = [
    {"restaurant_id": 53, "rating": 3},
    {"restaurant_id": 53, "rating": 1},
    {"restaurant_id": 3, "rating": 5},
    {"restaurant_id": 63, "rating": 1},
]


# equivalence partitioning

def test_popular_by_orders_returns_200():
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/popular-restaurants/orders")
    assert r.status_code == 200

def test_popular_by_orders_returns_correct_order():
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/popular-restaurants/orders")
    data = r.json()
    assert data[0]["restaurant_id"] == "30"  # 3 orders
    assert data[1]["restaurant_id"] == "16"  # 2 orders

def test_popular_by_orders_returns_correct_count():
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/popular-restaurants/orders")
    data = r.json()
    assert data[0]["total_orders"] == 3
    assert data[1]["total_orders"] == 2

def test_popular_by_rating_returns_200():
    with patch("app.services.popular_restaurants_service.load_all_reviews", return_value=MOCK_REVIEWS):
        r = client.get("/statistics/popular-restaurants/ratings")
    assert r.status_code == 200

def test_popular_by_rating_returns_correct_order():
    with patch("app.services.popular_restaurants_service.load_all_reviews", return_value=MOCK_REVIEWS):
        r = client.get("/statistics/popular-restaurants/ratings")
    data = r.json()
    assert data[0]["restaurant_id"] == 3      # rating 5.0
    assert data[1]["restaurant_id"] == 53     # rating 2.0

def test_popular_by_rating_returns_correct_average():
    with patch("app.services.popular_restaurants_service.load_all_reviews", return_value=MOCK_REVIEWS):
        r = client.get("/statistics/popular-restaurants/ratings")
    data = r.json()
    assert data[0]["average_rating"] == 5.0
    assert data[1]["average_rating"] == 2.0  # (3 + 1) / 2


# fault injection

def test_popular_by_orders_empty_returns_empty_list():
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=[]):
        r = client.get("/statistics/popular-restaurants/orders")
    assert r.json() == []

def test_popular_by_rating_empty_returns_empty_list():
    with patch("app.services.popular_restaurants_service.load_all_reviews", return_value=[]):
        r = client.get("/statistics/popular-restaurants/ratings")
    assert r.json() == []

def test_popular_by_orders_missing_restaurant_id_skipped():
    bad_orders = [
        {"delivery_delay": "10.0"},
        {"restaurant_id": "16", "delivery_delay": "5.0"},
    ]
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=bad_orders):
        r = client.get("/statistics/popular-restaurants/orders")
    assert r.json()[0]["restaurant_id"] == "16"

def test_popular_by_rating_invalid_rating_skipped():
    bad_reviews = [
        {"restaurant_id": 16, "rating": "not_a_number"},
        {"restaurant_id": 16, "rating": 4},
    ]
    with patch("app.services.popular_restaurants_service.load_all_reviews", return_value=bad_reviews):
        r = client.get("/statistics/popular-restaurants/ratings")
    assert r.json()[0]["average_rating"] == 4.0


# exception handling

def test_popular_by_orders_limit_parameter():
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/popular-restaurants/orders?limit=1")
    assert len(r.json()) == 1

def test_popular_by_rating_limit_parameter():
    with patch("app.services.popular_restaurants_service.load_all_reviews", return_value=MOCK_REVIEWS):
        r = client.get("/statistics/popular-restaurants/ratings?limit=1")
    assert len(r.json()) == 1

def test_popular_by_orders_invalid_limit():
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/popular-restaurants/orders?limit=0")
    assert r.status_code == 422


# mocking

def test_load_all_orders_is_called():
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=MOCK_ORDERS) as mock_load:
        client.get("/statistics/popular-restaurants/orders")
        assert mock_load.called

def test_load_all_reviews_is_called():
    with patch("app.services.popular_restaurants_service.load_all_reviews", return_value=MOCK_REVIEWS) as mock_load:
        client.get("/statistics/popular-restaurants/ratings")
        assert mock_load.called


# unit tests

def test_unit_popular_by_orders_correct_count():
    with patch("app.services.popular_restaurants_service.load_all_orders", return_value=MOCK_ORDERS):
        result = get_popular_restaurants_by_orders()
    assert result[0]["restaurant_id"] == "30"
    assert result[0]["total_orders"] == 3

def test_unit_popular_by_rating_correct_average():
    with patch("app.services.popular_restaurants_service.load_all_reviews", return_value=MOCK_REVIEWS):
        result = get_popular_restaurants_by_rating()
    assert result[0]["restaurant_id"] == 3
    assert result[0]["average_rating"] == 5.0