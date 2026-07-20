from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate
from app.services.device_service import device_service


router = APIRouter(
    prefix="/api/devices",
    tags=["Devices"],
)


# ==========================
# Create Device
# ==========================

@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
):
    try:
        return device_service.create_device(db, device)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ==========================
# Get All Devices
# ==========================

@router.get(
    "/",
    response_model=list[DeviceResponse],
)
def get_devices(
    db: Session = Depends(get_db),
):
    return device_service.get_devices(db)


# ==========================
# Get Device By ID
# ==========================

@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return device_service.get_device(db, device_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# ==========================
# Update Device
# ==========================

@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
)
def update_device(
    device_id: UUID,
    device: DeviceUpdate,
    db: Session = Depends(get_db),
):
    try:
        return device_service.update_device(
            db,
            device_id,
            device,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# ==========================
# Delete Device
# ==========================

@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        device_service.delete_device(db, device_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )