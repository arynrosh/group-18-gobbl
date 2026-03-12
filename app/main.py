from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.restaurant import router as menu_router
from app.routers.cost import router as cost_router
from app.routers.users import router as users_router
from app.routers.delivery import router as delivery_router
from app.routers.payment import router as payment_router
from app.routers.notification import router as notifications_router

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

@app.get("/")
def root():
    return {"message": "Gobbl API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}