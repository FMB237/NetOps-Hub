# SSH automation module using Netmiko
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from typing import Optional
import time


class SSHAutomation:
    """Handle SSH operations for network devices using Netmiko."""

    def __init__(self):
        self.connection = None
        self.device_info = None

    def connect(
        self,
        ip_address: str,
        port: int = 22,
        username: str = None,
        password: str = None,
        device_type: str = "auto",
        timeout: int = 10
    ) -> dict:
        """
        Establish SSH connection to a device using Netmiko.

        Args:
            ip_address: Device IP address
            port: SSH port (default 22)
            username: SSH username
            password: SSH password
            device_type: Device type (cisco_ios, juniper, etc.) - use 'auto' for detection
            timeout: Connection timeout in seconds

        Returns:
            dict: Connection result
        """
        # Determine device type based on vendor if auto
        if device_type == "auto":
            device_type = self._detect_device_type(username, password, ip_address, port)

        self.device_info = {
            "device_type": device_type,
            "host": ip_address,
            "port": port,
            "username": username,
            "password": password,
            "timeout": timeout,
        }

        start = time.time()

        try:
            self.connection = ConnectHandler(**self.device_info)

            latency = round((time.time() - start) * 1000, 2)

            return {
                "success": True,
                "connected": True,
                "latency": f"{latency} ms",
                "message": "SSH connection successful",
                "device_type": device_type,
            }
        except NetmikoTimeoutException:
            return {
                "success": False,
                "connected": False,
                "latency": None,
                "message": "Connection timed out",
            }
        except NetmikoAuthenticationException:
            return {
                "success": False,
                "connected": False,
                "latency": None,
                "message": "Authentication failed - invalid username or password",
            }
        except Exception as e:
            return {
                "success": False,
                "connected": False,
                "latency": None,
                "message": str(e),
            }

    def _detect_device_type(self, username: str, password: str, ip_address: str, port: int) -> str:
        """
        Detect device type by trying common device types.

        Returns:
            str: Device type
        """
        # Common device types to try
        device_types = [
            "cisco_ios",
            "cisco_s300",
            "cisco_asa",
            "juniper",
            "aruba_os",
            "hp_procurve",
            "dell_force10",
            "linux",
        ]

        for dtype in device_types:
            try:
                temp_device = {
                    "device_type": dtype,
                    "host": ip_address,
                    "port": port,
                    "username": username,
                    "password": password,
                    "timeout": 5,
                }
                conn = ConnectHandler(**temp_device)
                conn.disconnect()
                return dtype
            except:
                continue

        # Default to cisco_ios if detection fails
        return "cisco_ios"

    def execute_command(self, command: str) -> dict:
        """
        Execute a command on the connected device.

        Args:
            command: Command to execute

        Returns:
            dict: Command execution result
        """
        if not self.connection:
            return {
                "success": False,
                "output": None,
                "error": "Not connected to any device",
            }

        try:
            output = self.connection.send_command(command)

            return {
                "success": True,
                "output": output,
                "error": None,
                "command": command,
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e),
                "command": command,
            }

    def execute_commands(self, commands: list[str]) -> dict:
        """
        Execute multiple commands on the connected device.

        Args:
            commands: List of commands to execute

        Returns:
            dict: Command execution results
        """
        if not self.connection:
            return {
                "success": False,
                "outputs": None,
                "error": "Not connected to any device",
            }

        try:
            outputs = self.connection.send_config_set(commands)

            return {
                "success": True,
                "outputs": outputs,
                "error": None,
                "commands": commands,
            }
        except Exception as e:
            return {
                "success": False,
                "outputs": None,
                "error": str(e),
                "commands": commands,
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

    def get_show_ip_interface_brief(self) -> dict:
        """
        Get 'show ip interface brief' output from the device.

        Returns:
            dict: Show IP interface brief result
        """
        return self.execute_command("show ip interface brief")

    def save_config(self) -> dict:
        """
        Save configuration (copy run start for Cisco).

        Returns:
            dict: Save result
        """
        # Try common save commands
        commands = [
            "write memory",
            "copy running-config startup-config",
            "save",
        ]

        for cmd in commands:
            result = self.execute_command(cmd)
            if result["success"]:
                return {
                    "success": True,
                    "message": f"Configuration saved successfully",
                    "command": cmd,
                }

        return {
            "success": False,
            "message": "Failed to save configuration",
        }

    def disconnect(self):
        """Close the SSH connection."""
        if self.connection:
            self.connection.disconnect()
            self.connection = None
            self.device_info = None

    def test_connection(
        self,
        ip_address: str,
        port: int = 22,
        username: str = None,
        password: str = None,
        device_type: str = "auto"
    ) -> dict:
        """
        Test SSH connection to a device and get hostname.

        Args:
            ip_address: Device IP address
            port: SSH port
            username: SSH username
            password: SSH password
            device_type: Device type

        Returns:
            dict: Test result with hostname
        """
        result = self.connect(ip_address, port, username, password, device_type)

        if result["connected"]:
            # Try to get hostname
            hostname_result = self.execute_command("show hostname")
            if hostname_result["success"]:
                result["hostname"] = hostname_result["output"].strip()
            else:
                # Try alternative command
                hostname_result = self.execute_command("hostname")
                if hostname_result["success"]:
                    result["hostname"] = hostname_result["output"].strip()
                else:
                    result["hostname"] = None

            self.disconnect()

        return result


# Create singleton instance
ssh_automation = SSHAutomation()
