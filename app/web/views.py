#Our Frontend Router File

from fastapi import APIRouter,Depends,Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.device_service import device_service

# Let define the router 

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/devices")
def device_page(
    request: Request,
    db: Session = Depends(get_db)
):
    devices = device_service.get_devices(db)

    return templates.TemplateResponse(
        request=request,
        name="devices/index.html",
        context={
            "devices": devices,
        },
    )