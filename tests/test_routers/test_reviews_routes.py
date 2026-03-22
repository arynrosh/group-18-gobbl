from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import HTTPException
from app.main import app

client = TestClient(app)

def get_token(username: str, password: str) -> str:
    response = client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

FAKE_REVIEWS = [{
    "review_id": 1,
    "order_id": "15760aC",
    "restaurant_id": 53,
    "customer_id": "411b8170-4b51-48d6-8695-43cb3dbafc25",
    "rating": 3,
    "food_temperature": "Cold",
    "food_freshness": 4,
    "packaging_quality": 1,
    "food_condition": "Poor"
  },
  {
    "review_id": 2,
    "order_id": "aca6e0D",
    "restaurant_id": 53,
    "customer_id": "efecd3d9-44b9-4e43-b001-8d25c259d674",
    "rating": 1,
    "food_temperature": "Cold",
    "food_freshness": 5,
    "packaging_quality": 3,
    "food_condition": "Good"
  }
]
FAKE_REVIEW = {
    "review_id": 1,
    "order_id": "15760aC",
    "restaurant_id": 53,
    "customer_id": "411b8170-4b51-48d6-8695-43cb3dbafc25",
    "rating": 3,
    "food_temperature": "Cold",
    "food_freshness": 4,
    "packaging_quality": 1,
    "food_condition": "Poor"
  }

def test_customer_can_submit_review():
    customer_token = get_token("alice", "password123")
    with patch("app.services.review_service.create_review", return_value=FAKE_REVIEW):
        response = client.post("/reviews/",
                            json={"order_id": "15760aC", "rating": 3, "food_temperature": "Cold", "food_freshness": 4, "packaging_quality": 1, "food_condition": "Poor"},
                            headers=auth_header(customer_token)
        )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["message"] == "Review submitted successfully"
    assert data["review"]["rating"] == 3
    assert data["review"]["order_id"] == "15760aC"

def test_non_customer_cannot_submit_review():
    owner_token = get_token("bob", "securepass")
    response = client.post("/reviews/",
                           json={"order_id": "15760aC", "rating": 4, "food_temperature": "Warm", "food_freshness": 4, "packaging_quality": 4, "food_condition": "Good"},
                           headers=auth_header(owner_token)                 
    )
    assert response.status_code == 403, response.text

def test_get_reviews_for_restaurant():
    with patch("app.services.review_service.list_reviews_for_restaurant", return_value=FAKE_REVIEWS):
        response = client.get("/reviews/restaurant/53")

    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2
    assert data[0]["restaurant_id"] == 53
    assert data[1]["restaurant_id"] == 53

def test_get_reviews_for_restaurant_empty():
    with patch("app.services.review_service.list_reviews_for_restaurant", return_value=[]):
        response = client.get("/reviews/restaurant/1")
    assert response.status_code == 200
    assert response.json() == []

def test_get_average_rating_for_restaurant():
    with patch("app.services.review_service.get_average_rating", return_value=2.0):
        response = client.get("/reviews/restaurant/53/average")

    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"average_rating": 2.0}

def test_get_average_rating_for_restaurant_not_found():
    with patch("app.services.review_service.get_average_rating",
        side_effect=HTTPException(status_code=404, detail="No reviews found for this restaurant")
    ):
        response = client.get("/reviews/restaurant/9999/average")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "No reviews found for this restaurant"

