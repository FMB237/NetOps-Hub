# SSH automation module
import time
import paramiko
from typing import Optional


class SSHAutomation:
    """Handle SSH operations for network devices."""

    def __init__(self):
        self.client: Optional[paramiko.SSHClient] = None

    def connect(
        self,
        ip_address: str,
        port: int = 22,
        username: str = None,
        password: str = None,
        timeout: int = 10
    ) -> dict:
        """
        Establish SSH connection to a device.

        Args:
            ip_address: Device IP address
            port: SSH port (default 22)
            username: SSH username
            password: SSH password
            timeout: Connection timeout in seconds

        Returns:
            dict: Connection result
        """
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        start = time.time()

        try:
            self.client.connect(
                hostname=ip_address,
                port=port,
                username=username,
                password=password,
                timeout=timeout,
                banner_timeout=timeout,
                auth_timeout=timeout,
            )

            latency = round((time.time() - start) * 1000, 2)

            return {
                "success": True,
                "connected": True,
                "latency": f"{latency} ms",
                "message": "SSH connection successful",
            }
        except Exception as e:
            return {
                "success": False,
                "connected": False,
                "latency": None,
                "message": str(e),
            }

    def execute_command(self, command: str) -> dict:
        """
        Execute a command on the connected device.

        Args:
            command: Command to execute

        Returns:
            dict: Command execution result
        """
        if not self.client:
            return {
                "success": False,
                "output": None,
                "error": "Not connected to any device",
            }

        try:
            stdin, stdout, stderr = self.client.exec_command(command)

            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            return {
                "success": True,
                "output": output,
                "error": error if error else None,
                "command": command,
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e),
                "command": command,
            }

    def get_show_version(self) -> dict:
        """
        Get 'show version' output from the device.

        Returns:
            dict: Show version result
        """
        return self.execute_command("show version")

    def get_show_running_config(self) -> dict:
        """
        Get 'show running-config' output from the device.

        Returns:
            dict: Show running-config result
        """
        return self.execute_command("show running-config")

    def disconnect(self):
        """Close the SSH connection."""
        if self.client:
            self.client.close()
            self.client = None

    def test_connection(
        self,
        ip_address: str,
        port: int = 22,
        username: str = None,
        password: str = None
    ) -> dict:
        """
        Test SSH connection to a device and get hostname.

        Args:
            ip_address: Device IP address
            port: SSH port
            username: SSH username
            password: SSH password

        Returns:
            dict: Test result with hostname
        """
        result = self.connect(ip_address, port, username, password)

        if result["connected"]:
            # Try to get hostname
            hostname_result = self.execute_command("hostname")
            if hostname_result["success"]:
                result["hostname"] = hostname_result["output"]
            else:
                result["hostname"] = None

            self.disconnect()

        return result


# Create singleton instance
ssh_automation = SSHAutomation()
