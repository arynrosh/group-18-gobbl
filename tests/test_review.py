import pytest
from fastapi import HTTPException
from app.services import review_service
from app.schemas.review import ReviewCreate
from unittest.mock import patch

FAKE_REVIEWS = [  {
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

FAKE_ORDER = {
    "order_id": "odr-123",
    "customer_id": "cust-123",
    "restaurant_id": 10,
    "items": [
        {
            "menu_item_id": 1,
            "food_item": "Burger",
            "order_value": 41.17
        }
    ]
}


def test_get_review_returns_exisiting_review():
    with patch("app.services.review_service.load_all_reviews", return_value=FAKE_REVIEWS):
        review = review_service.get_review(1)
        assert review["review_id"] == 1
        assert review["restaurant_id"] == 53

def test_get_review_raises_404_for_missing_review():
    with patch("app.services.review_service.load_all_reviews", return_value=FAKE_REVIEWS):
        with pytest.raises(HTTPException) as exc:
            review_service.get_review(9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Review with id 9999 not found"

def test_create_review():
    fake_reviews = FAKE_REVIEWS.copy()
    review_data = ReviewCreate(
        order_id="odr-123",
        rating=4,
        food_temperature="Warm",
        food_freshness=4,
        packaging_quality=5,
        food_condition="Good"
    )

    with patch("app.services.review_service.load_all_reviews", return_value=fake_reviews), \
        patch("app.services.review_service.save_all_reviews") as mock_save, \
        patch("app.services.review_service.get_order_or_404", return_value=FAKE_ORDER):
        new_review = review_service.create_review(review_data)

        assert new_review["review_id"] >= 1
        assert new_review["order_id"] == "odr-123"
        assert new_review["restaurant_id"] == 10
        assert new_review["customer_id"] >= "cust-123"
        assert new_review["rating"] == 4
        assert new_review["food_temperature"] == "Warm"
        assert new_review["food_freshness"] == 4
        assert new_review["packaging_quality"] == 5
        assert new_review["food_condition"] == "Good"
        mock_save.assert_called_once()

def test_list_reviews_for_restaurant():
    with patch("app.services.review_service.load_all_reviews", return_value=FAKE_REVIEWS):
        reviews = review_service.list_reviews_for_restaurant(53)
        assert len(reviews) >= 1
        assert all(review["restaurant_id"] == 53 for review in reviews)

def test_list_reviews_for_restaurant_return_empty_list_when_none_exist():
    with patch("app.services.review_service.load_all_reviews", return_value=FAKE_REVIEWS):
        reviews = review_service.list_reviews_for_restaurant(9999)
        assert reviews == []

def test_get_average_rating():
    with patch("app.services.review_service.load_all_reviews", return_value=FAKE_REVIEWS):
        avg = review_service.get_average_rating(53)
        assert avg == 2.0

def test_average_rating_raises_404_when_no_reviews_exist():
    with patch("app.services.review_service.load_all_reviews", return_value=FAKE_REVIEWS):
        with pytest.raises(HTTPException) as exc:
            review_service.get_average_rating(9999)
        assert exc.value.status_code == 404
        assert exc.value.detail == "No reviews found for this restaurant"