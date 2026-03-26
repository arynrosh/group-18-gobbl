from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.cost_service import calculate_cost, TAX_RATE, DELIVERY_FEE
from app.schemas.order import Order, OrderItem

client = TestClient(app)

MOCK_ORDERS = [
    {
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "delivery_distance": 5,
        "assigned_driver_id": 0,
        "items": [{"food_item": "Tacos", "quantity": 2, "order_value": 10.00}],
        "sent": False
    },
    {
        "order_id": "f4d84dC",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 30,
        "delivery_distance": 8,
        "assigned_driver_id": 0,
        "items": [
            {"food_item": "Burger", "quantity": 2, "order_value": 10.00},
            {"food_item": "Pizza", "quantity": 1, "order_value": 12.00}
        ],
        "sent": False
    }
]

def get_customer_header():
    token = client.post("/auth/login", data={"username": "alice", "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_calculate_cost_valid_order():
    with patch("app.routers.cost.load_all_orders", return_value=MOCK_ORDERS):
        response = client.post("/cost/calculate/1d8e87M", headers=get_customer_header())
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 20.00
    assert data["tax"] == round(20.00 * TAX_RATE, 2)
    assert data["delivery_fee"] == DELIVERY_FEE
    assert data["total"] == round(20.00 + (20.00 * TAX_RATE) + DELIVERY_FEE, 2)


def test_calculate_cost_multiple_items():
    with patch("app.routers.cost.load_all_orders", return_value=MOCK_ORDERS):
        response = client.post("/cost/calculate/f4d84dC", headers=get_customer_header())
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 32.00
    assert data["total"] == round(32.00 + (32.00 * TAX_RATE) + DELIVERY_FEE, 2)


def test_calculate_cost_invalid_quantity():
    response = client.post("/cost/calculate/nonexistent_order", headers=get_customer_header())
    assert response.status_code == 404


def test_calculate_cost_invalid_order_value():
    response = client.post("/cost/calculate/nonexistent_order", headers=get_customer_header())
    assert response.status_code == 404


def test_calculate_cost_unauthorized_returns_401():
    response = client.post("/cost/calculate/1d8e87M")
    assert response.status_code == 401


def test_calculate_cost_wrong_role_returns_403():
    token = client.post(
        "/auth/login",
        data={"username": "bob", "password": "securepass"}
    ).json()["access_token"]
    restaurant_headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/cost/calculate/1d8e87M", headers=restaurant_headers)
    assert response.status_code == 403


def test_unit_calculate_cost_subtotal():
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        delivery_distance=5,
        assigned_driver_id=0,
        sent=False,
        items=[OrderItem(food_item="Tacos", quantity=2, order_value=10.00)]
    )
    result = calculate_cost(order)
    assert result.subtotal == 20.00


def test_unit_calculate_cost_tax():
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        delivery_distance=5,
        assigned_driver_id=0,
        sent=False,
        items=[OrderItem(food_item="Tacos", quantity=2, order_value=10.00)]
    )
    result = calculate_cost(order)
    assert result.tax == round(20.00 * TAX_RATE, 2)


def test_unit_calculate_cost_total():
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        delivery_distance=5,
        assigned_driver_id=0,
        sent=False,
        items=[OrderItem(food_item="Tacos", quantity=2, order_value=10.00)]
    )
    result = calculate_cost(order)
    assert result.total == round(20.00 + (20.00 * TAX_RATE) + DELIVERY_FEE, 2)