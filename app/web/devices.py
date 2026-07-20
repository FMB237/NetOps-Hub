# The router for our devices 

from fastapi import APIRouter,Depends,Request,Form
from fastapi.responses  import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm  import Session

# Let do some imports from the DB
from app.database.database import get_db
from app.services.device_service import device_service
from app.schemas.device import DeviceCreate
from app.models.enums import Vendor,DeviceType

router = APIRouter()

templates= Jinja2Templates(directory= "app/templates")

@router.get("/devices")
def device_page(request:Request,db: Session = Depends(get_db)):
    devices = device_service.get_devices(db)

    return templates.TemplateResponse(
        request=request,
        name="devices/index.html",
        context={
            "devices": devices,
            "active_page": "devices",
        }
        )

# Let also add a function for the devices routing 

@router.get("/devices")
def list_devices(request:Request,db: Session = Depends(get_db)):
    devices = device_service.get_devices(db)


    return templates.TemplateResponse(
        request=request,
        name="devices/index.html",
        context={
            "request":request,
            "devices": devices,
            "active_page":"devices"

        }
    )

# let create the devices form 

@router.get("/devices/create")
def create_devices_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="devices/create.html",
        context={
            "request":request,
            "vendors":Vendor,
            "device-type":DeviceType,
            "active_page":"devices"
        }
    )
