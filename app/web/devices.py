from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.device_service import device_service
from app.models.enums import Vendor, DeviceType

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/devices")
def list_devices(
    request: Request,
    db: Session = Depends(get_db),
):
    devices = device_service.get_devices(db)

    return templates.TemplateResponse(
        request=request,
        name="devices/index.html",
        context={
            "request": request,
            "devices": devices,
            "active_page": "devices",
        },
    )


@router.get("/devices/create")
def create_device_form(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="devices/create.html",
        context={
            "request": request,
            "vendors": Vendor,
            "device_types": DeviceType,
            "active_page": "devices",
        },
    )