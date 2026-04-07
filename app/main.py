from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.menu import router as menu_router 

from app.routers.cost import router as cost_router
from app.routers.users import router as users_router
from app.routers.delivery import router as delivery_router
from app.routers.payment import router as payment_router
from app.routers.notification import router as notifications_router
from app.routers.payment_methods import router as payment_methods_router
from app.routers.restaurant_search import router as restaurant_search_router
from app.routers.browsing import router as browsing_router
from app.routers.fulfillment import router as fulfillment_router
from app.routers.menu_search import router as menu_search_router
from app.routers.order_notification import router as order_notification_router
from app.routers.reviews import router as reviews_router
from app.routers.statistics import router as statistics_router 
from app.routers.popular_restaurants import router as popular_restaurants_router
from app.routers.order_router import router as order_router
from app.routers.diet_restrictions_router import router as diet_restrictions_router
from app.routers.recommendation_router import router as recommendation_router
from app.routers.discount_router import router as discount_router



app = FastAPI(
    title="Gobbl Food Delivery API",
    version="0.1.0",
    description="Backend API for the Gobbl food delivery platform."
)

app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(cost_router)
app.include_router(users_router)
app.include_router(delivery_router)
app.include_router(payment_router)
app.include_router(notifications_router)
app.include_router(payment_methods_router)
app.include_router(restaurant_search_router)
app.include_router(browsing_router)
app.include_router(fulfillment_router)
app.include_router(menu_search_router)
app.include_router(order_notification_router)
app.include_router(reviews_router)
app.include_router(statistics_router)
app.include_router(popular_restaurants_router)
app.include_router(order_router)
app.include_router(diet_restrictions_router)
app.include_router(recommendation_router)
app.include_router(discount_router)



@app.get("/")
def root():
    return {"message": "Gobbl API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}