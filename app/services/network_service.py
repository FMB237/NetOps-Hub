# Network service checker devices

import socket
import time
import subprocess
import platform

import paramiko


class NetworkService:

    def ping(self, ip_address: str, count: int = 4):
        """
        Ping a device to check if it's reachable.
        Returns ping statistics including packet loss and response time.
        """
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, str(count), ip_address]

        try:
            start = time.time()
            output = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                timeout=10
            )
            latency = round((time.time() - start) * 1000, 2)

            # Parse output for packet loss
            if "0% packet loss" in output.lower():
                packet_loss = 0
                # Try to get average response time
                try:
                    if "Average" in output:
                        avg_line = [line for line in output.split('\n') if 'Average' in line][0]
                        avg_time = float(avg_line.split('=')[1].split('ms')[0].strip())
                        avg_latency = round(avg_time, 2)
                    else:
                        avg_latency = round(latency / count, 2)
                except:
                    avg_latency = round(latency / count, 2)

                return {
                    "reachable": True,
                    "packet_loss": packet_loss,
                    "latency": f"{avg_latency} ms",
                    "message": "Device is reachable",
                    "raw_output": output,
                }
            else:
                # Parse packet loss percentage
                try:
                    loss_idx = output.lower().rfind("packet loss")
                    if loss_idx != -1:
                        loss_part = output[loss_idx:loss_idx+20]
                        if "%" in loss_part:
                            loss_pct = loss_part.split("%")[0].split()[-1]
                            packet_loss = int(loss_pct)
                        else:
                            packet_loss = 100
                    else:
                        packet_loss = 100
                except:
                    packet_loss = 100

                return {
                    "reachable": False,
                    "packet_loss": packet_loss,
                    "latency": None,
                    "message": f"Packet loss: {packet_loss}%",
                    "raw_output": output,
                }

        except subprocess.TimeoutExpired:
            return {
                "reachable": False,
                "packet_loss": 100,
                "latency": None,
                "message": "Ping timeout",
                "raw_output": None,
            }
        except Exception as e:
            return {
                "reachable": False,
                "packet_loss": 100,
                "latency": None,
                "message": str(e),
                "raw_output": None,
            }

    def test_connection(
        self,
        ip,
        port,
        username,
        password,
    ):
        """
        Test SSH connection to a device.
        Returns connection status, latency, and device hostname.
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

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

            latency = round((time.time() - start) * 1000, 2)

            stdin, stdout, stderr = ssh.exec_command("hostname")
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

    def check_port(self, ip: str, port: int):
        """
        Check if a specific port is open on a device.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        start = time.time()
        result = sock.connect_ex((ip, port))
        latency = round((time.time() - start) * 1000, 2)
        sock.close()
        return result == 0, latency


network_service = NetworkService()
