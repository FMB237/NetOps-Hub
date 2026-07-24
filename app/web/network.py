# Network web routes for UI
from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.services.device_service import device_service
from app.automation.backup import backup_automation

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/devices/{device_id}/execute")
def execute_command_form(
    device_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """Show command execution form."""
    device = device_service.get_device(db, device_id)

    if not device:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "Device not found"},
        )

    return templates.TemplateResponse(
        request=request,
        name="network/execute.html",
        context={
            "request": request,
            "device": device,
            "active_page": "devices",
        },
    )


@router.get("/devices/{device_id}/backup")
def backup_form(
    device_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """Show backup form and perform backup."""
    device = device_service.get_device(db, device_id)

    if not device:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "Device not found"},
        )

    # Check if username is available (password will be entered manually)
    if not device.username:
        return templates.TemplateResponse(
            request=request,
            name="network/backup.html",
            context={
                "request": request,
                "device": device,
                "error": "SSH username not configured for this device. Please add a username first.",
                "active_page": "devices",
            },
        )

    # Check if password is stored
    has_password = bool(device.password)

    return templates.TemplateResponse(
        request=request,
        name="network/backup.html",
        context={
            "request": request,
            "device": device,
            "has_password": has_password,
            "active_page": "devices",
        },
    )


@router.post("/devices/{device_id}/backup")
def perform_backup(
    device_id: UUID,
    request: Request,
    password: str = Form(None),
    db: Session = Depends(get_db),
):
    """Perform device configuration backup."""
    device = device_service.get_device(db, device_id)

    if not device:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "Device not found"},
        )

    # Use stored password if not provided in form
    if not password:
        password = device.password

    if not password:
        return templates.TemplateResponse(
            request=request,
            name="network/backup.html",
            context={
                "request": request,
                "device": device,
                "error": "No SSH password available. Please enter a password.",
                "active_page": "devices",
            },
        )

    # Perform backup
    result = backup_automation.backup_config(
        ip_address=device.ip_address,
        port=device.ssh_port,
        username=device.username,
        password=password,
        device_hostname=device.hostname,
    )

    if result["success"]:
        return templates.TemplateResponse(
            request=request,
            name="network/backup.html",
            context={
                "request": request,
                "device": device,
                "success": True,
                "backup": result,
                "active_page": "devices",
            },
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="network/backup.html",
            context={
                "request": request,
                "device": device,
                "error": result["message"],
                "active_page": "devices",
            },
        )


@router.get("/backups")
def list_backups(request: Request):
    """List all backup files."""
    backups = backup_automation.list_backups()

    return templates.TemplateResponse(
        request=request,
        name="network/backups.html",
        context={
            "request": request,
            "backups": backups,
            "active_page": "backups",
        },
    )
