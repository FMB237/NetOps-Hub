# Here we gonna defined our app db and models schema using pydantic

# Now let set up the devices responses
from uuid import UUID
from datetime import datetime


from pydantic import BaseModel,Field,ConfigDict,IPvAnyAddress
from app.models.enums import Devicetype,Vendor


# Let define the device base according to the device models
from pydantic import BaseModel, Field
from app.models.enums import Devicetype, Vendor

class DeviceBase(BaseModel):
    hostname: str = Field(..., max_length=100)
    ip_address: str
    vendor: Vendor
    model: str = Field(..., max_length=100)
    device_type: Devicetype
    operating_system: str = Field(..., max_length=100)
    ssh_port: int = Field(default=22, ge=1, le=65535)
    username: str | None = None
    location: str | None = None
    notes: str | None = None


# For creating new devices
class DeviceCreate(DeviceBase):
    pass

# For devices update

class DeviceUpdate(BaseModel):
    hostname: str | None = None
    ip_address: str | None = None
    vendor: Vendor | None = None
    model: str | None = None
    device_type: Devicetype | None = None
    operating_system: str | None = None
    ssh_port: int | None = None
    username: str | None = None
    location: str | None = None
    notes: str | None = None

class DeviceResponse(DeviceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config= ConfigDict (
         from_attributes=True
    )
     
    