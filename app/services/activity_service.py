# Activity service for logging events
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.models.activity import Activity
from app.models.enums import ActivityType, ActivityLevel


class ActivityService:
    """Service for logging activities."""

    def log_activity(
        self,
        db: Session,
        activity_type: ActivityType,
        message: str,
        level: ActivityLevel = ActivityLevel.INFO,
        details: str = None,
        device_id: UUID = None,
        device_hostname: str = None,
        user: str = None,
        ip_address: str = None,
    ) -> Activity:
        """
        Log an activity to the database.

        Args:
            db: Database session
            activity_type: Type of activity
            message: Activity message
            level: Activity level (info, warning, error, etc.)
            details: Additional details
            device_id: Related device UUID
            device_hostname: Related device hostname
            user: User who performed the action
            ip_address: IP address of the request

        Returns:
            Activity: The created activity log
        """
        activity = Activity(
            activity_type=activity_type,
            level=level,
            message=message,
            details=details,
            device_id=device_id,
            device_hostname=device_hostname,
            user=user,
            ip_address=ip_address,
            created_at=datetime.now(),
        )

        db.add(activity)
        db.commit()
        db.refresh(activity)

        return activity

    def get_recent_activities(
        self,
        db: Session,
        limit: int = 50,
        activity_type: ActivityType = None,
        level: ActivityLevel = None,
    ) -> list:
        """
        Get recent activities.

        Args:
            db: Database session
            limit: Number of activities to return
            activity_type: Filter by activity type
            level: Filter by activity level

        Returns:
            list: List of activities
        """
        query = db.query(Activity)

        if activity_type:
            query = query.filter(Activity.activity_type == activity_type)

        if level:
            query = query.filter(Activity.level == level)

        return query.order_by(Activity.created_at.desc()).limit(limit).all()

    def get_activities_by_device(
        self,
        db: Session,
        device_id: UUID,
        limit: int = 50,
    ) -> list:
        """
        Get activities for a specific device.

        Args:
            db: Database session
            device_id: Device UUID
            limit: Number of activities to return

        Returns:
            list: List of activities for the device
        """
        return (
            db.query(Activity)
            .filter(Activity.device_id == device_id)
            .order_by(Activity.created_at.desc())
            .limit(limit)
            .all()
        )


# Create singleton instance
activity_service = ActivityService()
