# This is the network router Api for testing connections
from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.schemas.network import ConnectedTestRequest, ConnectedTestResponse
from app.services.network_service import network_service

router = APIRouter(prefix="/api/network", tags=["Network"])


# Ping request/response models
class PingRequest(BaseModel):
    ip_address: str
    count: int = 4


class PingResponse(BaseModel):
    reachable: bool
    packet_loss: int
    latency: str | None = None
    message: str


# Let create our post test route

@router.post('/test', response_model=ConnectedTestResponse)
def test_connection(request: ConnectedTestRequest):

    return network_service.test_connection(
        request.ip_address,
        request.port,
        request.username,
        request.password,
    )


@router.post('/ping', response_model=PingResponse)
def ping_device(request: PingRequest):
    """Ping a device to check if it's reachable."""
    result = network_service.ping(request.ip_address, request.count)
    return PingResponse(
        reachable=result["reachable"],
        packet_loss=result["packet_loss"],
        latency=result["latency"],
        message=result["message"],
    )


@router.get('/ping')
def ping_device_get(
    ip_address: str = Query(..., description="IP address to ping"),
    count: int = Query(4, description="Number of ping packets"),
):
    """Ping a device to check if it's reachable (GET request)."""
    result = network_service.ping(ip_address, count)
    return result
