# This is the network router Api for testing connections
from fastapi import APIRouter

from app.schemas.network import (ConnectedTestRequest,ConnectedTestResponse)
from app.services.network_service import network_service

router = APIRouter(prefix="/api/network",tags=["Network"])

# Let create our post test route 

@router.post('/test',response_model=ConnectedTestResponse)
def test_connection(request: ConnectedTestRequest):
    return network_service.test_connection(request.ip_address,request.port)
