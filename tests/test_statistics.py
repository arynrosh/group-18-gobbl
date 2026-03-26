from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.statistics_service import get_average_delivery_times

client = TestClient(app)

MOCK_ORDERS = [
    {"restaurant_id": "16", "delivery_time": 10.0},
    {"restaurant_id": "16", "delivery_time": 20.0},
    {"restaurant_id": "30", "delivery_time": 15.0},
]

def get_admin_token():
    r = client.post("/auth/login", data={"username": "admin", "password": "adminpass"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# equivalence partitioning

def test_delivery_times_returns_200():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert r.status_code == 200

def test_per_restaurant_average_is_correct():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert r.json()["per_restaurant"]["16"] == 15.0
    assert r.json()["per_restaurant"]["30"] == 15.0

def test_system_wide_average_is_correct():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert r.json()["system_wide_average_minutes"] == 15.0

def test_response_contains_expected_keys():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert "per_restaurant" in r.json()
    assert "system_wide_average_minutes" in r.json()

# fault injection

def test_empty_orders_returns_empty_result():
    with patch("app.services.statistics_service.load_all_orders", return_value=[]):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert r.json()["per_restaurant"] == {}
    assert r.json()["system_wide_average_minutes"] is None

def test_invalid_delay_value_is_skipped():
    bad_orders = [
        {"restaurant_id": "16", "delivery_time": None},
        {"restaurant_id": "16", "delivery_time": 10.0},
    ]
    with patch("app.services.statistics_service.load_all_orders", return_value=bad_orders):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert r.json()["per_restaurant"]["16"] == 10.0

def test_missing_delay_field_is_skipped():
    bad_orders = [
        {"restaurant_id": "16"},
        {"restaurant_id": "16", "delivery_time": 10.0},
    ]
    with patch("app.services.statistics_service.load_all_orders", return_value=bad_orders):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert r.json()["per_restaurant"]["16"] == 10.0

# exception handling

def test_single_order_does_not_crash():
    single = [{"restaurant_id": "50", "delivery_time": 8.5}]
    with patch("app.services.statistics_service.load_all_orders", return_value=single):
        r = client.get("/statistics/delivery-times", headers=get_admin_token())
    assert r.status_code == 200
    assert r.json()["system_wide_average_minutes"] == 8.5

# unit tests

def test_unit_per_restaurant_average():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        result = get_average_delivery_times()
    assert result["per_restaurant"]["16"] == 15.0

def test_unit_system_wide_average():
    with patch("app.services.statistics_service.load_all_orders", return_value=MOCK_ORDERS):
        result = get_average_delivery_times()
    assert result["system_wide_average_minutes"] == 15.0

def test_unit_empty_returns_none_system_wide():
    with patch("app.services.statistics_service.load_all_orders", return_value=[]):
        result = get_average_delivery_times()
    assert result["system_wide_average_minutes"] is None