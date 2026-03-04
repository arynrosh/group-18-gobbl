from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import TokenResponse, UserInfo
from app.services.auth_service import login_user, get_user_info
from app.auth.dependencies import get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    #Accepts username and password, returns a JWT token if credentials are valid
    return login_user(form_data.username, form_data.password)


@router.get("/me", response_model=UserInfo)
def get_profile(current_user: dict = Depends(get_current_user)):
   
   # Returns the currently logged-in user's info
    #Requires valid bearer token in the authorization header
    return get_user_info(current_user)


@router.get("/admin-only")
def admin_only(current_user: dict = Depends(require_role("admin"))):
    return {"message": f"Welcome admin {current_user.get('sub')}"}


@router.get("/owner-only")
def owner_only(current_user: dict = Depends(require_role("restaurant_owner"))):
    return {"message": f"Welcome {current_user.get('sub')}"}
