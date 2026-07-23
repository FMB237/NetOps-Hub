from fastapi import APIRouter, Depends, Request,Form,Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from uuid import UUID
from fastapi import HTTPException

from app.database.database import get_db
from app.services.device_service import device_service
from app.models.enums import Vendor, DeviceType
from app.schemas.device import DeviceCreate,DeviceUpdate

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")



@router.get("/devices")
def list_devices(
    request: Request,
    db: Session = Depends(get_db),
    search: str | None = Query(default=None),
    vendor: str | None = Query(default=None, description="Vendor", alias="vendor"),
    device_type: str | None = Query(default=None, description="Device Type", alias="device_type"),
):
    # Fix: Accept str, convert to Enum if not None or empty
    vendor = vendor or None
    device_type = device_type or None
    from app.models.enums import Vendor, DeviceType
    if vendor is not None:
        vendor = Vendor(vendor)
    if device_type is not None:
        device_type = DeviceType(device_type)

    devices = device_service.search_devices(
        db,
        search,
        vendor,
        device_type,
    )
    return templates.TemplateResponse(
        request=request,
        name="devices/index.html",
        context={
            "request": request,
            "devices": devices,
            "vendors": Vendor,
            "device_types": DeviceType,
            "search": search,
            "selected_vendor": vendor,
            "selected_type": device_type,
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

# let add a post request for editing 
@router.post("/devices/{device_id}/edit")
def update_device(
    device_id: UUID,
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

    device = DeviceUpdate(
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

    device_service.update_device(
        db,
        device_id,
        device,
    )

    return RedirectResponse(
        url="/devices",
        status_code=303,
    )    


# adding delete route
@router.post("/devices/{device_id}/delete")
def delete_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):

    device_service.delete_device(
        db,
        device_id,
    )

    return RedirectResponse(
        url="/devices",
        status_code=303,
    )


# Device Details page
@router.get("/devices/{device_id}")
def device_details(
    device_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    device = device_service.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return templates.TemplateResponse(
        request=request,
        name="devices/details.html",
        context={
            "request": request,
            "device": device,
            "active_page": "devices",
        },
    )


