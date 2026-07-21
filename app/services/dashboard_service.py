# Let add the dashboard_services
from sqlalchemy.orm import Session
from app.models.device import Device

class DashboardService:
    def get_dashboard_stats(self, db: Session):
        devices = db.query(Device).all()
        total_devices = len(devices)
        vendors = {}
        recent_devices = sorted(
            devices,
            key=lambda d: d.created_at,
            reverse=True
        )[:5]
        for device in devices:
            vendor = str(device.vendor)
            vendors[vendor] = vendors.get(vendor, 0) + 1
        return {
            "total_devices": total_devices,
            "vendors": vendors,
            "recent_devices": recent_devices,
            "online_devices": 0,
            "offline_devices": total_devices,
        }


dashboard_service = DashboardService()