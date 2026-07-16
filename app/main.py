from fastapi import FastAPI

from app.database.base import Base
from app.database.database import engine
from app.api.device_router import router as device_router
# from app.services.device_service import device_service
# from app.repositories.device_repository import device_repository

# Import all models
import app.models

app.include_router(device_router)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NetOps Hub")


@app.get("/")
def home():
    return{
        "message":"Hello NetHub-Ops"
    }