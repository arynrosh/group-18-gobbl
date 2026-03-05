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

@pytest.fixture(autouse=True)
def seed_test_users():
    # seeding known users before each test, restoring empty state after
    with DATA_PATH.open("w") as f:
        json.dump(TEST_USERS, f)
    yield
    with DATA_PATH.open("w") as f:
        json.dump([], f)
