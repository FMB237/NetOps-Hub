# This is where we gonna put the network_router.py file 
from pydantic import BaseModel,Field

class ConnectedTestRequest(BaseModel):
    ip_address : str
    port : int = Field(default=22)


class ConnectedTestResponse(BaseModel):
    reachable : bool
    port_open : bool
    latency : str | None = None 
    message : str
