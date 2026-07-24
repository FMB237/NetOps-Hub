# Backup automation module
import os
from datetime import datetime
from typing import Optional
from app.automation.ssh import SSHAutomation


class BackupAutomation:
    """Handle configuration backup operations for network devices."""

    def __init__(self, backup_dir: str = "app/backups"):
        self.backup_dir = backup_dir
        self.ssh = SSHAutomation()
        self._ensure_backup_dir()

    def _ensure_backup_dir(self):
        """Ensure backup directory exists."""
        os.makedirs(self.backup_dir, exist_ok=True)

    def _sanitize_filename(self, hostname: str) -> str:
        """Create safe filename from hostname."""
        return hostname.replace(" ", "_").replace("/", "_").replace("\\", "_")

    def backup_config(
        self,
        ip_address: str,
        port: int = 22,
        username: str = None,
        password: str = None,
        device_hostname: str = None
    ) -> dict:
        """
        Backup running configuration from a network device.

        Args:
            ip_address: Device IP address
            port: SSH port
            username: SSH username
            password: SSH password
            device_hostname: Device hostname (optional, will try to get from device)

        Returns:
            dict: Backup result with file path
        """
        # Connect to device
        connect_result = self.ssh.connect(ip_address, port, username, password)

        if not connect_result["connected"]:
            return {
                "success": False,
                "message": f"Failed to connect: {connect_result['message']}",
                "file_path": None,
            }

        # Get hostname if not provided
        if not device_hostname:
            hostname_result = self.ssh.execute_command("hostname")
            if hostname_result["success"]:
                device_hostname = hostname_result["output"]
            else:
                device_hostname = ip_address

        # Get running config
        config_result = self.ssh.get_show_running_config()

        if not config_result["success"]:
            self.ssh.disconnect()
            return {
                "success": False,
                "message": f"Failed to get config: {config_result.get('error', 'Unknown error')}",
                "file_path": None,
            }

        # Create backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_hostname = self._sanitize_filename(device_hostname)
        filename = f"{safe_hostname}_{timestamp}.cfg"
        file_path = os.path.join(self.backup_dir, filename)

        # Write config to file
        try:
            with open(file_path, "w") as f:
                f.write(config_result["output"])

            file_size = os.path.getsize(file_path)

            self.ssh.disconnect()

            return {
                "success": True,
                "message": "Backup completed successfully",
                "file_path": file_path,
                "filename": filename,
                "device_hostname": device_hostname,
                "ip_address": ip_address,
                "timestamp": timestamp,
                "file_size": file_size,
            }
        except Exception as e:
            self.ssh.disconnect()
            return {
                "success": False,
                "message": f"Failed to save backup: {str(e)}",
                "file_path": None,
            }

    def list_backups(self) -> list:
        """
        List all backup files.

        Returns:
            list: List of backup files with metadata
        """
        backups = []

        try:
            for filename in os.listdir(self.backup_dir):
                file_path = os.path.join(self.backup_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    backups.append({
                        "filename": filename,
                        "file_path": file_path,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    })
        except Exception as e:
            return [{"error": str(e)}]

        # Sort by modified date (newest first)
        backups.sort(key=lambda x: x.get("modified", ""), reverse=True)
        return backups

    def get_backup_content(self, filename: str) -> Optional[str]:
        """
        Get content of a backup file.

        Args:
            filename: Name of the backup file

        Returns:
            str: File content or None if error
        """
        file_path = os.path.join(self.backup_dir, filename)
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception:
            return None

    def delete_backup(self, filename: str) -> dict:
        """
        Delete a backup file.

        Args:
            filename: Name of the backup file

        Returns:
            dict: Delete result
        """
        file_path = os.path.join(self.backup_dir, filename)
        try:
            os.remove(file_path)
            return {
                "success": True,
                "message": f"Deleted {filename}",
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }


# Create singleton instance
backup_automation = BackupAutomation()
