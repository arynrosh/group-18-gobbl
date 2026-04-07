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

def get_diet_restrictions_or_404(username: str, all_restrictions: list) -> dict:
    user_entry = next(
        (u for u in all_restrictions if u.get("username") == username),
        None,
    )

    if user_entry:
        return user_entry

    user = get_user_or_404(username)
    if not create_diet_restrictions(user["role"]):
        raise HTTPException(
            status_code=404,
            detail=f"User {username} not eligible for diet restrictions",
        )

    new_entry = {
        "username": username,
        "diet_restrictions": [],
    }
    all_restrictions.append(new_entry)
    return new_entry

def add_diet_restriction(username: str, restriction: str) -> dict:
    all_restrictions = load_all_diet_restrictions()

    user = get_diet_restrictions_or_404(username, all_restrictions)

    if restriction not in user["diet_restrictions"]:
        user["diet_restrictions"].append(restriction)

    save_all_diet_restrictions(all_restrictions)
    return user

def remove_diet_restriction(username: str, restriction: str) -> dict:
    all_restrictions = load_all_diet_restrictions()

    user = get_diet_restrictions_or_404(username, all_restrictions)

    if restriction in user["diet_restrictions"]:
        user["diet_restrictions"].remove(restriction)

    save_all_diet_restrictions(all_restrictions)
    return user