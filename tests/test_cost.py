from fastapi.testclient import TestClient
from app.main import app
from app.services.cost_service import calculate_cost, TAX_RATE, DELIVERY_FEE
from app.schemas.order import Order, OrderItem

client = TestClient(app)


def test_calculate_cost_valid_order():
    # Test that a valid order returns correct cost breakdown
    response = client.post("/cost/calculate", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "items": [
            {"food_item": "Tacos", "quantity": 2, "order_value": 10.00}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 20.00
    assert data["tax"] == round(20.00 * TAX_RATE, 2)
    assert data["delivery_fee"] == DELIVERY_FEE
    assert data["total"] == round(20.00 + (20.00 * TAX_RATE) + DELIVERY_FEE, 2)

def test_calculate_cost_multiple_items():
    # Test that orders with multiple items calculate subtotal correctly
    response = client.post("/cost/calculate", json={
        "order_id": "f4d84dC",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 30,
        "items": [
            {"food_item": "Burger", "quantity": 2, "order_value": 10.00},
            {"food_item": "Pizza", "quantity": 1, "order_value": 12.00}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 32.00
    assert data["total"] == round(32.00 + (32.00 * TAX_RATE) + DELIVERY_FEE, 2)

def test_calculate_cost_invalid_quantity():
    # Test that an order with invalid quantity returns 422
    response = client.post("/cost/calculate", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "items": [
            {"food_item": "Tacos", "quantity": 0, "order_value": 10.00}
        ]
    })
    assert response.status_code == 422

def test_calculate_cost_invalid_order_value():
    # Test that an order with invalid price returns 422
    response = client.post("/cost/calculate", json={
        "order_id": "1d8e87M",
        "customer_id": "9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        "restaurant_id": 16,
        "items": [
            {"food_item": "Tacos", "quantity": 1, "order_value": -5.00}
        ]
    })
    assert response.status_code == 422


def test_unit_calculate_cost_subtotal():
    # Test service function calculates subtotal correctly
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        items=[
            OrderItem(food_item="Tacos", quantity=2, order_value=10.00)
        ]
    )
    result = calculate_cost(order)
    assert result.subtotal == 20.00

def test_unit_calculate_cost_tax():
    # Test service function calculates tax correctly
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        items=[
            OrderItem(food_item="Tacos", quantity=2, order_value=10.00)
        ]
    )
    result = calculate_cost(order)
    assert result.tax == round(20.00 * TAX_RATE, 2)

def test_unit_calculate_cost_total():
    # Test service function calculates total correctly
    order = Order(
        order_id="1d8e87M",
        customer_id="9c6dbfcb-72c5-4cc4-9f76-29200f0efda7",
        restaurant_id=16,
        items=[
            OrderItem(food_item="Tacos", quantity=2, order_value=10.00)
        ]
    )
    result = calculate_cost(order)
    assert result.total == round(20.00 + (20.00 * TAX_RATE) + DELIVERY_FEE, 2)