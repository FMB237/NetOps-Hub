# Network API router
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional

from app.automation.ping import ping_automation
from app.automation.ssh import ssh_automation
from app.automation.backup import backup_automation

router = APIRouter(prefix="/api/network", tags=["Network"])


# Request/Response models
class PingRequest(BaseModel):
    ip_address: str
    count: int = 4


class PingResponse(BaseModel):
    success: bool
    reachable: bool
    packet_loss: int
    latency: Optional[str] = None
    message: str


class SSHTestRequest(BaseModel):
    ip_address: str
    port: int = 22
    username: str
    password: str


class SSHTestResponse(BaseModel):
    success: bool
    connected: bool
    latency: Optional[str] = None
    message: str
    hostname: Optional[str] = None


class ExecuteCommandRequest(BaseModel):
    ip_address: str
    port: int = 22
    username: str
    password: str
    command: str


class ExecuteCommandResponse(BaseModel):
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    command: str


class BackupRequest(BaseModel):
    ip_address: str
    port: int = 22
    username: str
    password: str
    device_hostname: Optional[str] = None


class BackupResponse(BaseModel):
    success: bool
    message: str
    file_path: Optional[str] = None
    filename: Optional[str] = None


# Ping endpoints
@router.post("/ping", response_model=PingResponse)
def ping_device(request: PingRequest):
    """Ping a device to check if it's reachable."""
    result = ping_automation.ping(request.ip_address, request.count)
    return PingResponse(
        success=result["success"],
        reachable=result["reachable"],
        packet_loss=result["packet_loss"],
        latency=result["latency"],
        message=result["message"],
    )


@router.get("/ping")
def ping_device_get(
    ip_address: str = Query(..., description="IP address to ping"),
    count: int = Query(4, description="Number of ping packets"),
):
    """Ping a device (GET request)."""
    return ping_automation.ping(ip_address, count)


# SSH Test endpoints
@router.post("/test", response_model=SSHTestResponse)
def test_ssh_connection(request: SSHTestRequest):
    """Test SSH connection to a device."""
    result = ssh_automation.test_connection(
        ip_address=request.ip_address,
        port=request.port,
        username=request.username,
        password=request.password,
    )
    return SSHTestResponse(
        success=result["success"],
        connected=result["connected"],
        latency=result.get("latency"),
        message=result["message"],
        hostname=result.get("hostname"),
    )


# Execute command endpoints
@router.post("/execute", response_model=ExecuteCommandResponse)
def execute_command(request: ExecuteCommandRequest):
    """Execute a command on a network device via SSH."""
    # First connect
    connect_result = ssh_automation.connect(
        ip_address=request.ip_address,
        port=request.port,
        username=request.username,
        password=request.password,
    )

    if not connect_result["connected"]:
        return ExecuteCommandResponse(
            success=False,
            output=None,
            error=connect_result["message"],
            command=request.command,
        )

    # Execute command
    result = ssh_automation.execute_command(request.command)
    ssh_automation.disconnect()

    return ExecuteCommandResponse(
        success=result["success"],
        output=result.get("output"),
        error=result.get("error"),
        command=request.command,
    )


# Backup endpoints
@router.post("/backup", response_model=BackupResponse)
def backup_config(request: BackupRequest):
    """Backup running configuration from a network device."""
    result = backup_automation.backup_config(
        ip_address=request.ip_address,
        port=request.port,
        username=request.username,
        password=request.password,
        device_hostname=request.device_hostname,
    )
    return BackupResponse(
        success=result["success"],
        message=result["message"],
        file_path=result.get("file_path"),
        filename=result.get("filename"),
    )


@router.get("/backups")
def list_backups():
    """List all backup files."""
    return {"backups": backup_automation.list_backups()}


@router.get("/backups/{filename}")
def get_backup_content(filename: str):
    """Get content of a specific backup file."""
    content = backup_automation.get_backup_content(filename)
    if content is None:
        return {"error": "Backup file not found"}
    return {"filename": filename, "content": content}
