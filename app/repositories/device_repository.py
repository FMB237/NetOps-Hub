from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import or_ # Let import a new library 
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceRepository:

    def create(self, db: Session, device: DeviceCreate) -> Device:
        db_device = Device(**device.model_dump())

        db.add(db_device)
        db.commit()
        db.refresh(db_device)

        return db_device

    def get_all(self, db: Session):
        return db.query(Device).all()

    def get_by_id(self, db: Session, device_id: UUID):
        return (
            db.query(Device)
            .filter(Device.id == device_id)
            .first()
        )

    def get_by_hostname(self, db: Session, hostname: str):
        return (
            db.query(Device)
            .filter(Device.hostname == hostname)
            .first()
        )

    def delete(self, db: Session, device: Device):
        db.delete(device)
        db.commit()

    def update(
        self,
        db: Session,
        db_device: Device,
        device: DeviceUpdate,
    ):
        update_data = device.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_device, key, value)

        db.commit()
        db.refresh(db_device)

        return db_device
    # Let add a new function for searching in our app
    def search(self,db: Session,search : str | None = None, vendor=None,device_type=None):
        query = db.query(Device)
        if search:
            query = query.filter(
                or_(
                    Device.hostname.ilike(f'%{search}%'),
                    Device.ip_address.ilike(f'%{search}%'),
                    Device.operating_system.ilike(f'%{search}%')
                )
            )  
        if vendor : 
            query = query.filter(Device.vendor == vendor)
        if  device_type:
             query = query.filter(Device.device_type == device_type)
        return query.order_by(Device.hostname).all()





device_repository = DeviceRepository()