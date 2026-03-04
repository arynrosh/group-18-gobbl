from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.browsing_demo import router as browsing_router

app = FastAPI()

@app.get("/health/")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(browsing_router)
