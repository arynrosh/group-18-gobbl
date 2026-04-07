import pytest
from fastapi import HTTPException
from app.services import review_service
from app.schemas.review import ReviewCreate
from unittest.mock import patch

FAKE_REVIEWS = [
    {
        "review_id": 1,
        "order_id": "15760aC",
        "restaurant_id": 53,
        "customer_id": "411b8170-4b51-48d6-8695-43cb3dbafc25",
        "food_temperature": "Cold",
        "food_freshness": 4,
        "packaging_quality": 1,
        "food_condition": "Poor",
        "item_ratings": [
            {
                "menu_item_id": 1,
                "food_item": "Burger",
                "customer_rating": 3,
                "written_review": "It was okay."
            }
        ]
    },
    {
        "review_id": 2,
        "order_id": "aca6e0D",
        "restaurant_id": 53,
        "customer_id": "efecd3d9-44b9-4e43-b001-8d25c259d674",
        "food_temperature": "Cold",
        "food_freshness": 5,
        "packaging_quality": 3,
        "food_condition": "Good",
        "item_ratings": [
            {
                "menu_item_id": 1,
                "food_item": "Burger",
                "customer_rating": 1,
                "written_review": "Worst burger ever!"
            }
        ]
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
            "quantity": 1,
            "order_value": 41.17
        }
    ]
}

FAKE_MENU_ITEM = {
    "menu_item_id": 1,
    "restaurant_id": 10,
    "food_item": "Burger",
    "order_value": 41.17
}

FAKE_MENU_ITEMS = [
    {
        "menu_item_id": 1,
        "restaurant_id": 53,
        "customer_rating": 3.0
    },
    {
        "menu_item_id": 2,
        "restaurant_id": 53,
        "customer_rating": 1.0
    }
]

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

def test_get_reviewable_items_for_order_returns_items():
    with patch("app.services.review_service.get_order_or_404", return_value=FAKE_ORDER):
        items = review_service.get_reviewable_items_for_order("odr-123")

    assert len(items) == 1
    assert items[0]["menu_item_id"] == 1
    assert items[0]["food_item"] == "Burger"
    assert items[0]["customer_rating"] == None
    assert items[0]["written_review"] == None

def test_get_reviewable_items_for_order_raises_404_when_no_items():
    empty_order = {
        "order_id": "odr-123",
        "customer_id": "cust-456",
        "restaurant_id": 10,
        "items": []
    }

    with patch("app.services.review_service.get_order_or_404", return_value=empty_order):
        with pytest.raises(HTTPException) as exc:
            review_service.get_reviewable_items_for_order("odr-123")

    assert exc.value.status_code == 404
    assert exc.value.detail == "No items found for this order"

def test_create_review():
    fake_reviews = FAKE_REVIEWS.copy()
    review_data = ReviewCreate(
        order_id="odr-123",
        food_temperature="Warm",
        food_freshness=4,
        packaging_quality=5,
        food_condition="Good",
        item_ratings=[
            {
                "menu_item_id": 1,
                "food_item": "Burger",
                "customer_rating": 4,
                "written_review": "Burger was juicy and fresh."
            }
        ]
    )

    with patch("app.services.review_service.load_all_reviews", return_value=fake_reviews), \
         patch("app.services.review_service.save_all_reviews") as mock_save, \
         patch("app.services.review_service.get_order_or_404", return_value=FAKE_ORDER), \
         patch("app.services.review_service.get_menu_item", return_value=FAKE_MENU_ITEM), \
         patch("app.services.review_service.recalculate_menu_item_ratings") as mock_recalculation:
        new_review = review_service.create_review(review_data)

        assert new_review["review_id"] >= 1
        assert new_review["order_id"] == "odr-123"
        assert new_review["restaurant_id"] == 10
        assert new_review["customer_id"] == "cust-123"
        assert new_review["food_temperature"] == "Warm"
        assert new_review["food_freshness"] == 4
        assert new_review["packaging_quality"] == 5
        assert new_review["food_condition"] == "Good"
        assert new_review["item_ratings"][0]["menu_item_id"] == 1
        assert new_review["item_ratings"][0]["food_item"] == "Burger"
        assert new_review["item_ratings"][0]["customer_rating"] == 4
        assert new_review["item_ratings"][0]["written_review"] == "Burger was juicy and fresh."
        mock_save.assert_called_once()
        mock_recalculation.assert_called_once()

def test_create_review_raises_400_when_menu_item_wrong_restaurant():
    review_data = ReviewCreate(
        order_id="odr-123",
        food_temperature="Warm",
        food_freshness=4,
        packaging_quality=5,
        food_condition="Good",
        item_ratings=[
            {
                "menu_item_id": 1,
                "food_item": "Burger",
                "customer_rating": 4,
                "written_review": "Burger was juicy and fresh."
            }
        ]
    )

    wrong_restaurant_menu_item = {
        "menu_item_id": 1,
        "restaurant_id": 9999,
        "food_item": "Burger",
        "order_value": 41.17
    }

    with patch("app.services.review_service.load_all_reviews", return_value=[]), \
         patch("app.services.review_service.get_order_or_404", return_value=FAKE_ORDER), \
         patch("app.services.review_service.get_menu_item", return_value=wrong_restaurant_menu_item):
        with pytest.raises(HTTPException) as exc:
            review_service.create_review(review_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Menu item 1 does not match the restaurant for this order"

def test_create_review_raises_400_when_menu_item_not_in_order():
    review_data = ReviewCreate(
        order_id="odr-123",
        food_temperature="Warm",
        food_freshness=4,
        packaging_quality=5,
        food_condition="Good",
        item_ratings=[
            {
                "menu_item_id": 2,
                "food_item": "Fries",
                "customer_rating": 4
            }
        ]
    )

    menu_item = {
        "menu_item_id": 2,
        "restaurant_id": 10,
        "food_item": "Fries",
        "order_value": 9.99
    }

    with patch("app.services.review_service.load_all_reviews", return_value=[]), \
         patch("app.services.review_service.get_order_or_404", return_value=FAKE_ORDER), \
         patch("app.services.review_service.get_menu_item", return_value=menu_item):
        with pytest.raises(HTTPException) as exc:
            review_service.create_review(review_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Menu item 2 was not part of order odr-123"

def test_list_reviews_for_restaurant():
    with patch("app.services.review_service.load_all_reviews", return_value=FAKE_REVIEWS):
        reviews = review_service.list_reviews_for_restaurant(53)
        assert len(reviews) >= 1
        assert all(review["restaurant_id"] == 53 for review in reviews)

def test_list_reviews_for_restaurant_return_empty_list_when_none_exist():
    with patch("app.services.review_service.load_all_reviews", return_value=FAKE_REVIEWS):
        reviews = review_service.list_reviews_for_restaurant(9999)
        assert reviews == []

def test_recalculate_menu_item_ratings_updates_average_and_count():
    fake_reviews = [
        {
            "item_ratings": [
                {"menu_item_id": 1, "food_item": "Burger", "customer_rating": 3}
            ]
        },
        {
            "item_ratings": [
                {"menu_item_id": 1, "food_item": "Burger", "customer_rating": 5}
            ]
        }
    ]

    fake_menu_items = [
        {
            "menu_item_id": 1,
            "restaurant_id": 53,
            "food_item": "Burger",
            "customer_rating": None,
            "rating_count": 0
        }
    ]

    with patch("app.services.review_service.load_all_reviews", return_value=fake_reviews), \
         patch("app.services.review_service.load_all_menu_items", return_value=fake_menu_items), \
         patch("app.services.review_service.save_all_menu_items") as mock_save:
        review_service.recalculate_menu_item_ratings()

    assert fake_menu_items[0]["customer_rating"] == 4.0
    assert fake_menu_items[0]["rating_count"] == 2
    mock_save.assert_called_once()

def test_recalculate_menu_item_ratings_ignores_none_ratings():
    fake_reviews = [
        {
            "item_ratings": [
                {"menu_item_id": 1, "food_item": "Burger", "customer_rating": None}
            ]
        },
        {
            "item_ratings": [
                {"menu_item_id": 1, "food_item": "Burger", "customer_rating": 5}
            ]
        }
    ]

    fake_menu_items = [
        {
            "menu_item_id": 1,
            "restaurant_id": 53,
            "food_item": "Burger",
            "customer_rating": None,
            "rating_count": 0
        }
    ]

    with patch("app.services.review_service.load_all_reviews", return_value=fake_reviews), \
         patch("app.services.review_service.load_all_menu_items", return_value=fake_menu_items), \
         patch("app.services.review_service.save_all_menu_items"):
        review_service.recalculate_menu_item_ratings()

    assert fake_menu_items[0]["customer_rating"] == 5.0
    assert fake_menu_items[0]["rating_count"] == 1

def test_get_average_rating():
    with patch("app.services.review_service.load_all_menu_items", return_value=FAKE_MENU_ITEMS):
        avg = review_service.get_average_rating_for_restaurant(53)
        assert avg == 2.0

def test_average_rating_raises_404_when_no_reviews_exist():
    with patch("app.services.review_service.load_all_menu_items", return_value=[]):
        with pytest.raises(HTTPException) as exc:
            review_service.get_average_rating_for_restaurant(9999)
        assert exc.value.status_code == 404
        assert exc.value.detail == "No rated menu items found for this restaurant"