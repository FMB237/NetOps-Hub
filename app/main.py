from fastapi import FastAPI

from app.database.base import Base
from app.database.database import engine

# Import all models
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NetOps Hub")