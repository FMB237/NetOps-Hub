# This is the device_service file 
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.device import Device
from app.repositories.device_repository import device_repository
from app.schemas.device import DeviceCreate,DeviceUpdate

class DeviceService:
    """Business logic for Network devices"""

    def create_device(self,db:Session,device:DeviceCreate) -> Device : 
        existing = device_repository.get_by_hostname(db,device.hostname)
        if existing:
            raise ValueError("A device with this hostname already exists")

        return device_repository.create(db,device)

    def get_devices(self,db:Session):
        return device_repository.get_all(db)   

    def get_device(self,db:Session,device_id:UUID):
        device = device_repository.get_by_id(db,device_id)

        if not device:
            raise ValueError('Device not found')

        return device

    def update_device(self,db:Session,device_id:UUID,update:DeviceUpdate):
        device = self.get_device(db,device_id)

        return device_repository.update(db,device,update)

    def delete_device(self,db:Session, device_id:UUID):
        device = self.get_device(db,device_id)

        return device_repository.delete(db,device)                  
    def search_devices(self,db: Session,search : str | None = None,vendor= None,device_type=None):
        return device_repository.search(db,search,vendor,device_type,)

device_service= DeviceService()
