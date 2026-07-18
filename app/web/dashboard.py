from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.device_service import device_service

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    devices = device_service.get_devices(db)
    total_devices = len(devices)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "devices": devices,
            "total_devices": total_devices,
            "active_page": "dashboard"
        },
    )
