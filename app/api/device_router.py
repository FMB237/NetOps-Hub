# Let start Building our APIs

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.device import DeviceCreate
from app.schemas.device import DeviceResponse
from app.schemas.device import DeviceUpdate
from app.services.device_service import device_service

# Let add our app router 

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)

# Let start adding our app 
@router.post("/",response_model=DeviceResponse,status_code=201)
def create_device(device:DeviceCreate, db: Session = Depends(get_db)):

    try :    
        return device_service.create_device(db,device)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))



           

# Get All Devices
@router.get("/",response_model=list[DeviceResponse])
def get_devices(db:Session = Depends(get_db)):
    return device_service.get_devices(db)


# Get Device by ID

@router.get("/{device_id}",response_model=DeviceResponse)
def get_device(device_id:UUID,db:Session = Depends(get_db)):
    try:
        return device_service.get_devices(db,device_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))


# Update Device

@router.put("/{device_id}",response_model=DeviceResponse)
def update_device(device_id: UUID,device: DeviceUpdate, db: Session = Depends(get_db)):
    try:
        return device_service.update_device(db,device_id,device)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))


@router.delete('/{device_id}',status_code=204)
def delete_device(device_id:UUID, db: Session = Depends(get_db)):
    try:
        device_service.delete_device(db,device_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))

