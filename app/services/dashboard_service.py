# Let add the dashboard_services
from sqlalchemy.orm import Session
from app.models.device import Device
from datetime import datetime, timedelta

class DashboardService:
    def get_dashboard_stats(self, db: Session):
        devices = db.query(Device).all()
        total_devices = len(devices)

        # Vendor breakdown
        vendors = {}
        for device in devices:
            vendor = str(device.vendor)
            vendors[vendor] = vendors.get(vendor, 0) + 1

        # Device type breakdown
        device_types = {}
        for device in devices:
            dtype = str(device.device_type)
            device_types[dtype] = device_types.get(dtype, 0) + 1

        # Recent devices (last 5)
        recent_devices = sorted(
            devices,
            key=lambda d: d.created_at or datetime.min,
            reverse=True
        )[:5]

        # Recently added this week
        one_week_ago = datetime.now() - timedelta(days=7)
        recently_added = sum(
            1 for d in devices
            if d.created_at and d.created_at >= one_week_ago
        )

        # Recently updated this week
        recently_updated = sum(
            1 for d in devices
            if d.updated_at and d.updated_at >= one_week_ago
        )

        return {
            "total_devices": total_devices,
            "vendors": vendors,
            "device_types": device_types,
            "recent_devices": recent_devices,
            "recently_added": recently_added,
            "recently_updated": recently_updated,
            "online_devices": 0,
            "offline_devices": total_devices,
        }


dashboard_service = DashboardService()