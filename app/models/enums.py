from enum import Enum

# Let create our class defines

class DeviceType(str,Enum):
    ROUTER = "Router"
    SWITCH = "Switch"
    FIREWALL = "Firewall"
    SERVER = "Server"
    ACCESS_POINT= "Access_Point"
    LOAD_BALANCER = "Load_Balancer"

# Let add the vendor which are mainly the devices type builders


class Vendor(str,Enum):
    CISCO = "Cisco"
    LINUX = "Linux"
    HUAWEI = "Huawei"
    PAOLATO = "PAOLATO"
    MIKROTIK = "MikroTik"
    FORTINET = "Fortinet"
    ARISTA = "Arista"


# Activity types for logging
class ActivityType(str, Enum):
    # Device actions
    DEVICE_CREATED = "device_created"
    DEVICE_UPDATED = "device_updated"
    DEVICE_DELETED = "device_deleted"
    DEVICE_VIEWED = "device_viewed"

    # Automation actions
    PING = "ping"
    SSH_TEST = "ssh_test"
    COMMAND_EXECUTED = "command_executed"
    BACKUP_CREATED = "backup_created"
    BACKUP_VIEWED = "backup_viewed"
    BACKUP_DELETED = "backup_deleted"

    # User actions
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    SETTINGS_CHANGED = "settings_changed"

    # System actions
    SYSTEM_START = "system_start"
    SYSTEM_ERROR = "system_error"


# Activity levels for logging
class ActivityLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
