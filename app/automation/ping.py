# Ping automation module
import subprocess
import platform
import time


class PingAutomation:
    """Handle ping operations for network devices."""

    def ping(self, ip_address: str, count: int = 4):
        """
        Ping a device to check if it's reachable.

        Args:
            ip_address: The IP address to ping
            count: Number of ping packets to send

        Returns:
            dict: Ping results including reachable status, latency, packet loss
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
            total_latency = round((time.time() - start) * 1000, 2)

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
                        avg_latency = round(total_latency / count, 2)
                except:
                    avg_latency = round(total_latency / count, 2)

                return {
                    "success": True,
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
                    "success": True,
                    "reachable": False,
                    "packet_loss": packet_loss,
                    "latency": None,
                    "message": f"Packet loss: {packet_loss}%",
                    "raw_output": output,
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "reachable": False,
                "packet_loss": 100,
                "latency": None,
                "message": "Ping timeout",
                "raw_output": None,
            }
        except Exception as e:
            return {
                "success": False,
                "reachable": False,
                "packet_loss": 100,
                "latency": None,
                "message": str(e),
                "raw_output": None,
            }

    def ping_multiple(self, ip_addresses: list[str], count: int = 4):
        """
        Ping multiple devices.

        Args:
            ip_addresses: List of IP addresses to ping
            count: Number of ping packets per device

        Returns:
            dict: Results for each IP address
        """
        results = {}
        for ip in ip_addresses:
            results[ip] = self.ping(ip, count)
        return results


# Create singleton instance
ping_automation = PingAutomation()
