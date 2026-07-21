from fastapi import APIRouter, Depends, Request,Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from uuid import UUID

from app.database.database import get_db
from app.services.device_service import device_service
from app.models.enums import Vendor, DeviceType
from app.schemas.device import DeviceCreate

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


    # adding the post request 
@router.post("/devices/create")
def create_device(
    hostname: str = Form(...),
    ip_address: str = Form(...),
    vendor: Vendor = Form(...),
    device_type: DeviceType = Form(...),
    model: str = Form(...),
    operating_system: str = Form(...),
    ssh_port: int = Form(22),
    username: str | None = Form(None),
    location: str | None = Form(None),
    notes: str | None = Form(None),
    db: Session = Depends(get_db),
):
    device = DeviceCreate(
        hostname=hostname,
        ip_address=ip_address,
        vendor=vendor,
        device_type=device_type,
        model=model,
        operating_system=operating_system,
        ssh_port=ssh_port,
        username=username,
        location=location,
        notes=notes,
    )

    device_service.create_device(db, device)

    return RedirectResponse(
        url="/devices",
        status_code=303,
    )


# Let add and edit route 
@router.get("/devices/{device_id}/edit")
def edit_device_form(
    device_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    device = device_service.get_device(
        db,
        device_id,
    )

    return templates.TemplateResponse(
        request=request,
        name="devices/edit.html",
        context={
            "request": request,
            "device": device,
            "vendors": Vendor,
            "device_types": DeviceType,
            "form_action": f"/devices/{device_id}/edit",
            "submit_label": "Save Changes",
            "active_page": "devices",
        },
    )