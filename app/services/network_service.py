# Network service checker devices

# Let used some new python models
"""import socket
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

network_service = NetworkService()"""


import socket
import time

import paramiko


class NetworkService:

    def test_connection(
        self,
        ip,
        port,
        username,
        password,
    ):

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        start = time.time()

        try:

            ssh.connect(
                hostname=ip,
                port=port,
                username=username,
                password=password,
                timeout=5,
                banner_timeout=5,
                auth_timeout=5,
            )

            latency = round(
                (time.time() - start) * 1000,
                2,
            )

            stdin, stdout, stderr = ssh.exec_command(
                "hostname"
            )

            hostname = stdout.read().decode().strip()

            ssh.close()

            return {
                "reachable": True,
                "port_open": True,
                "latency": f"{latency} ms",
                "message": "SSH connection successful",
                "hostname": hostname,
            }
        except Exception as e:

            return {
                "reachable": False,
                "port_open": False,
                "latency": None,
                "message": str(e),
                "hostname": None,
            }
          


network_service = NetworkService()