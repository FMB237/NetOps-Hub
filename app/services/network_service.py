# Network service checker file 

# Let used some new python models
import socket
import time 

class NetworkService:
    def check_port(self,ip:str, port:int ):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(2)
        start = time.time()
        result = sock.connect_ex((ip,port))
        latency = round((time.time() - start) * 1000,2)
        sock.close()
        return result == 0,latency

# Adding Test Connections 

    def test_connection(self, ip: str, port: int):
        opened, latency = self.check_port(ip, port)
        return {
            "reachable": opened,
            "port_open": opened,
            "latency": f"{latency} ms",
            "message": (
                "Connection successful"
                if opened
                else "Unable to reach device"
            ),
        }

network_service = NetworkService()