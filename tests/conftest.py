import pytest
import json
from pathlib import Path

TEST_USERS = [
    {"username": "alice", "email": "alice@example.com", "password": "password123", "role": "customer"},
    {"username": "bob", "email": "bob@example.com", "password": "securepass", "role": "restaurant_owner"},
    {"username": "dave", "email": "dave@example.com", "password": "driverpass", "role": "driver"},
    {"username": "admin", "email": "admin@example.com", "password": "adminpass", "role": "admin"},
]

DATA_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "users.json"
PAYMENTS_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "payments.json"
ORDERS_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "orders.json"
STATUS_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "status.json"
ORDERITEMS_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "OrderItem.json"
DISCOUNTS_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "discounts.json"


@pytest.fixture(autouse=True)
def seed_test_users():
    original = DATA_PATH.read_text() if DATA_PATH.exists() else "[]"
    with DATA_PATH.open("w") as f:
        json.dump(TEST_USERS, f)
    yield
    DATA_PATH.write_text(original)


@pytest.fixture(autouse=True)
def restore_payments():
    original = PAYMENTS_PATH.read_text() if PAYMENTS_PATH.exists() else "[]"
    yield
    PAYMENTS_PATH.write_text(original)


@pytest.fixture(autouse=True)
def restore_orders():
    original = ORDERS_PATH.read_text() if ORDERS_PATH.exists() else "[]"
    yield
    ORDERS_PATH.write_text(original)


@pytest.fixture(autouse=True)
def restore_status():
    original = STATUS_PATH.read_text() if STATUS_PATH.exists() else "[]"
    yield
    STATUS_PATH.write_text(original)


@pytest.fixture(autouse=True)
def restore_orderitems():
    original = ORDERITEMS_PATH.read_text() if ORDERITEMS_PATH.exists() else "[]"
    yield
    ORDERITEMS_PATH.write_text(original)

@pytest.fixture(autouse=True)
def restore_discounts():
    original = DISCOUNTS_PATH.read_text() if DISCOUNTS_PATH.exists() else "[]"
    yield
    DISCOUNTS_PATH.write_text(original)
