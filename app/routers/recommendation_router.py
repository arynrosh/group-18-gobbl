from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.recommendation import RecommendedItem
from app.services.recommendation_service import get_recommendations
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/{customer_id}", response_model=List[RecommendedItem])
def recommend_items(customer_id: str, limit: int = 5, current_user: dict = Depends(get_current_user)):
    
    if current_user.get("role") not in ["customer", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied.")

    results = get_recommendations(customer_id, limit)

    if not results:
        raise HTTPException(status_code=404, detail="No recommendations found. Customer may have no order history.")

    return results