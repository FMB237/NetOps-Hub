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


