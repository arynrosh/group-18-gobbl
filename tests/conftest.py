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


@pytest.fixture(autouse=True)
def seed_test_users():
    # saving original contents before test
    original = DATA_PATH.read_text() if DATA_PATH.exists() else "[]"
    # seeding known users for the test
    with DATA_PATH.open("w") as f:
        json.dump(TEST_USERS, f)
    yield
    # restoring original contents after test
    DATA_PATH.write_text(original)


@pytest.fixture(autouse=True)
def restore_payments():
    # saving original payments before test
    original = PAYMENTS_PATH.read_text() if PAYMENTS_PATH.exists() else "[]"
    yield
    # restoring original payments after test
    PAYMENTS_PATH.write_text(original)