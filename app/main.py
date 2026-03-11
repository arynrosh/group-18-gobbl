from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.restaurant import router as menu_router
<<<<<<< HEAD
from app.routers.restaurant_search import router as restaurant_search_router
from app.routers.menu_search import router as menu_search_router
=======
from app.routers.users import router as users_router
>>>>>>> origin/main

app = FastAPI(
    title="Gobbl Food Delivery API",
    version="0.1.0",
    description="Backend API for the Gobbl food delivery platform."
)

app.include_router(auth_router)
app.include_router(menu_router)
<<<<<<< HEAD
app.include_router(restaurant_search_router)
app.include_router(menu_search_router)
=======
app.include_router(users_router)
>>>>>>> origin/main

@app.get("/")
def root():
    return {"message": "Gobbl API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}