from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.base import Base
from app.database.database import engine
from app.api.device_router import router as device_router

# Import all models so SQLAlchemy can register them
import app.models

app = FastAPI(
    title="NetOps Hub",
    description="Network Operations and Automation Platform",
    version="1.0.0",
)

# Include API routes
app.include_router(device_router)

# Create database tables
Base.metadata.create_all(bind=engine)

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }