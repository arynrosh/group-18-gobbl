from fastapi import HTTPException
from app.repositories.users_repo import load_all_users
from app.schemas.diet_restrictions import diet_restrictions
from app.repositories.diet_restrictions_repo import load_all_diet_restrictions, save_all_diet_restrictions


def create_diet_restrictions(role: str) -> None:
    if role != "customer":
        return False
    return True

def get_user_or_404(username: str) -> dict:
    users = load_all_users()
    user = next((u for u in users if u.get("username") == username), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {username} not found")
    return user

def get_diet_restrictions_or_404(username: str) -> dict:
    diet_restrictions = load_all_diet_restrictions()
    user_restrictions = next((u for u in diet_restrictions if u.get("username") == username), None)
    if not user_restrictions:
        user = get_user_or_404(username)
        user_role = user["role"]
        if create_diet_restrictions(user_role):
            list = []
            new_diet_restrictions = {
                "username": username,
                "diet_restrictions": list
            }
            return new_diet_restrictions
        else:
            raise HTTPException(status_code=404, detail=f"User {username} not found with or eligible for diet_restrictions")
    return user_restrictions

def add_diet_restriction(username: str, restriction: str) -> dict:
    users = load_all_diet_restrictions()
    user = get_diet_restrictions_or_404(username)
    restrict = user["diet_restrictions"]
    restrict.append(restriction)
    user["diet_restrictions"] = restrict
    save_all_diet_restrictions(users)
    #return user["diet_restrictions"]

"""def add_to_order(order_id: str, restaurant_id: int, food_item: str, quantity: int) -> dict:
    orders = load_all_orders()
    order = _get_order_or_404(order_id, orders)

    if order.get("sent"):
        raise HTTPException(status_code=400, detail="Cannot modify order after it has been sent")
    
    menu_item = get_menu_item(food_item, restaurant_id)

    if order["restaurant_id"] != menu_item["restaurant_id"]:
        raise HTTPException(
            status_code=400,
            detail="Item does not belong to this order's restaurant"
        )        

    new_item = {
        "food_item": menu_item["food_item"],
        "quantity": quantity,
        "order_value": menu_item["order_value"],
    }

    order["items"].append(new_item)
    save_all_orders(orders)
    return order"""

def remove_diet_restriction(username: str, restriction: str) -> dict:
    users = load_all_diet_restrictions()
    user = get_diet_restrictions_or_404(username)
    
    if restriction in user["diet_restrictions"]:
        user["diet_restrictions"].remove(restriction)
    save_all_diet_restrictions(users)
    #return user["diet_restrictions"]