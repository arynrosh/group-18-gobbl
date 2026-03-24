from fastapi.testclient import TestClient
from app.main import app
from app.services.cost_service import calculate_cost, TAX_RATE, DELIVERY_FEE
from app.schemas.order import Order, OrderItem

client = TestClient(app)


def test_calculate_cost_valid_order():
    response = client.post("/cost/calculate", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "driver_distance": 0,
        "assigned_driver_id": 0,
        "sent": False,
        "items": [
            {"food_item": "Tacos", "quantity": 2, "order_value": 10.00, "resturant_id": 16}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 20.00
    assert data["tax"] == round(20.00 * TAX_RATE, 2)
    assert data["delivery_fee"] == DELIVERY_FEE
    assert data["total"] == round(20.00 + (20.00 * TAX_RATE) + DELIVERY_FEE, 2)


def test_calculate_cost_multiple_items():
    response = client.post("/cost/calculate", json={
        "order_id": "f4d84dC",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 30,
        "driver_distance": 0,
        "assigned_driver_id": 0,
        "sent": False,
        "items": [
            {"food_item": "Burger", "quantity": 2, "order_value": 10.00, "resturant_id": 16},
            {"food_item": "Pizza", "quantity": 1, "order_value": 12.00, "resturant_id": 16}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 32.00
    assert data["total"] == round(32.00 + (32.00 * TAX_RATE) + DELIVERY_FEE, 2)


def test_calculate_cost_invalid_quantity():
    response = client.post("/cost/calculate", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "driver_distance": 0,
        "assigned_driver_id": 0,
        "sent": False,
        "items": [
            {"food_item": "Tacos", "quantity": 0, "order_value": 10.00, "resturant_id": 16}
        ]
    })
    assert response.status_code == 422


def test_calculate_cost_invalid_order_value():
    response = client.post("/cost/calculate", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "driver_distance": 0,
        "assigned_driver_id": 0,
        "sent": False,
        "items": [
            {"food_item": "Tacos", "quantity": 1, "order_value": -5.00, "resturant_id": 16}
        ]
    })
    assert response.status_code == 422


def test_unit_calculate_cost_subtotal():
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        driver_distance=0,
        assigned_driver_id=0,
        sent=False,
        items=[OrderItem(food_item="Tacos", quantity=2, order_value=10.00, resturant_id=16)]
    )
    result = calculate_cost(order)
    assert result.subtotal == 20.00


def test_unit_calculate_cost_tax():
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        driver_distance=0,
        assigned_driver_id=0,
        sent=False,
        items=[OrderItem(food_item="Tacos", quantity=2, order_value=10.00, resturant_id=16)]
    )
    result = calculate_cost(order)
    assert result.tax == round(20.00 * TAX_RATE, 2)


def test_unit_calculate_cost_total():
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        driver_distance=0,
        assigned_driver_id=0,
        sent=False,
        items=[OrderItem(food_item="Tacos", quantity=2, order_value=10.00, resturant_id=16)]
    )
    result = calculate_cost(order)
    assert result.total == round(20.00 + (20.00 * TAX_RATE) + DELIVERY_FEE, 2)