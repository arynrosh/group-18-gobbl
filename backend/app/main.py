from fastapi import FastAPI
from routers.auth import router as auth_router
app = FastAPI()
@app.get("/health/")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
