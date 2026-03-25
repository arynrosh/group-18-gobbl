import pytest
from fastapi import HTTPException
from app.services import menu_service
from app.schemas.menu import MenuItemCreate, MenuItemUpdate
from unittest.mock import patch

FAKE_MENU = [
    {
    "menu_item_id": 1,
    "restaurant_id": 53,
    "restaurant_name": "Cactus Club",
    "cuisine": "American",
    "food_item": "Burger",
    "order_value": 41.17,
    "customer_rating": 4,
    "delivery_time_actual": 10.74
    },
    {
    "menu_item_id": 2,
    "restaurant_id": 53,
    "restaurant_name": "Cactus Club",
    "cuisine": "American",
    "food_item": "Steak",
    "order_value": 25.67,
    "customer_rating": 3,
    "delivery_time_actual": 10.74
    },
    {
    "menu_item_id": 3,
    "restaurant_id": 3,
    "restaurant_name": "Twisted Tomato",
    "cuisine": "Italian",    
    "food_item": "Pasta",
    "order_value": 37.25,
    "customer_rating": 5,
    "delivery_time_actual": 9.09
    },
    {
    "menu_item_id": 4,
    "restaurant_id": 63,
    "restaurant_name": "Antoli Soulaki",
    "cuisine": "Greek",
    "food_item": "Salad",
    "order_value": 18.08,
    "customer_rating": 1,
    "delivery_time_actual": -0.34
    },
    {
    "menu_item_id": 5,
    "restaurant_id": 3,
    "restaurant_name": "Twisted Tomato",
    "cuisine": "Italian", 
    "food_item": "Pizza",
    "order_value": 32.99,
    "customer_rating": 3,
    "delivery_time_actual": 12.56
    }
]

def test_get_menu_item_returns_existing_item():
    with patch("app.services.menu_service.load_all_menu_items", return_value=FAKE_MENU):
        item = menu_service.get_menu_item("Burger", 53)
        assert item["food_item"] == "Burger"
        assert item["restaurant_id"] == 53

def test_get_menu_item_raises_404_for_missing_item():
    with patch("app.services.menu_service.load_all_menu_items", return_value=FAKE_MENU):
        with pytest.raises(HTTPException) as exc:
            menu_service.get_menu_item("Burger", 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Menu item Burger not found for restaurant 9999"

def test_validate_item_belongs_to_restaurant_raises_403():
    item = {
        "menu_item_id": 1,
        "restaurant_id": 53
    }

    with pytest.raises(HTTPException) as exc:
        menu_service.validate_item_belongs_to_restaurant(item, 9999)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Menu item does not belong to this restaurant"

def test_list_menu_items_without_filters():
    with patch("app.services.menu_service.load_all_menu_items", return_value=FAKE_MENU):
        items = menu_service.list_menu_items(3)
        assert len(items) == 2
        assert items[0]["food_item"] == "Pasta"
        assert items[1]["food_item"] == "Pizza"

def test_list_menu_filters_by_price_tier():
    with patch("app.services.menu_service.load_all_menu_items" , return_value=FAKE_MENU):
        items = menu_service.list_menu_items(53, price_tier="$$$$")
        assert len(items) == 1
        assert items[0]["food_item"] == "Burger"

def test_list_menu_items_filters_by_min_rating():
    with patch("app.services.menu_service.load_all_menu_items" , return_value=FAKE_MENU):
        items = menu_service.list_menu_items(53, min_rating=3.0)
        assert len(items) == 2
        assert items[0]["food_item"] == "Burger"
        assert items[1]["food_item"] == "Steak"

def test_list_menu_items_filters_when_no_match():
    with patch("app.services.menu_service.load_all_menu_items" , return_value=FAKE_MENU):
        items = menu_service.list_menu_items(53, price_tier="$")
        assert items == []

def test_create_menu_item():
    fake_menu = FAKE_MENU.copy()
    item_data = MenuItemCreate(
        restaurant_name="Soup House",
        cuisine="Comfort Food",
        food_item="Soup",
        order_value=12.50
    )

    with patch("app.services.menu_service.load_all_menu_items", return_value=fake_menu), \
        patch("app.services.menu_service.save_all_menu_items") as mock_save:
        item = menu_service.create_menu_item(10, item_data)

        assert item["menu_item_id"] == 6
        assert item["restaurant_id"] == 10
        assert item["restaurant_name"] == "Soup House"
        assert item["cuisine"] == "Comfort Food"
        assert item["food_item"] == "Soup"
        assert item["order_value"] == 12.50
        mock_save.assert_called_once()

def test_update_menu_item():
    fake_menu = FAKE_MENU.copy()
    item_data = MenuItemUpdate(
        restaurant_name="Cactus Club",
        cuisine="American",
        food_item="Spicy Burger",
        order_value=50.00
    )

    with patch("app.services.menu_service.load_all_menu_items", return_value=fake_menu), \
        patch("app.services.menu_service.save_all_menu_items") as mock_save:
        item = menu_service.update_menu_item(53, 1, item_data)

        assert item["restaurant_name"] == "Cactus Club"
        assert item["cuisine"] == "American"
        assert item["food_item"] == "Spicy Burger"
        assert item["order_value"] == 50.00
        mock_save.assert_called_once()

def test_update_menu_item_raises_404_for_missing_item():
    fake_menu = FAKE_MENU.copy()
    item_data = MenuItemUpdate(
        restaurant_name="Cactus Club",
        cuisine="American",        
        food_item="Spicy Burger",
        order_value=50.00
    )

    with patch("app.services.menu_service.load_all_menu_items", return_value=fake_menu):
        with pytest.raises(HTTPException) as exc:
            menu_service.update_menu_item(53, 9999, item_data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Menu item with id 9999 not found"

def test_delete_menu_item():
    fake_menu = FAKE_MENU.copy()

    with patch("app.services.menu_service.load_all_menu_items", return_value=fake_menu), \
        patch("app.services.menu_service.save_all_menu_items") as mock_save:
        
        menu_service.delete_menu_item(53, 1)
        menu_ids = [item["menu_item_id"] for item in fake_menu]

        assert 1 not in menu_ids
        mock_save.assert_called_once()

def test_delete_menu_item_raises_404_for_missing_item():
    fake_menu = FAKE_MENU.copy()

    with patch("app.services.menu_service.load_all_menu_items", return_value=fake_menu):
        with pytest.raises(HTTPException) as exc:
            menu_service.delete_menu_item(53, 9999)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Menu item with id 9999 not found"

