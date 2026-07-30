# Activity API router
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.database.database import get_db
from app.services.activity_service import activity_service
from app.models.enums import ActivityType, ActivityLevel

router = APIRouter(prefix="/api/activities", tags=["Activities"])


class ActivityResponse(BaseModel):
    id: UUID
    activity_type: str
    level: str
    message: str
    details: Optional[str] = None
    device_id: Optional[UUID] = None
    device_hostname: Optional[str] = None
    user: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=list[ActivityResponse])
def get_activities(
    limit: int = Query(default=50, le=100),
    activity_type: Optional[str] = Query(default=None, description="Filter by activity type"),
    level: Optional[str] = Query(default=None, description="Filter by level"),
    db: Session = Depends(get_db),
):
    """Get recent activities."""
    at = ActivityType(activity_type) if activity_type else None
    lvl = ActivityLevel(level) if level else None

    activities = activity_service.get_recent_activities(
        db=db,
        limit=limit,
        activity_type=at,
        level=lvl,
    )
    return activities


@router.get("/device/{device_id}", response_model=list[ActivityResponse])
def get_device_activities(
    device_id: UUID,
    limit: int = Query(default=50, le=100),
    db: Session = Depends(get_db),
):
    """Get activities for a specific device."""
    activities = activity_service.get_activities_by_device(
        db=db,
        device_id=device_id,
        limit=limit,
    )
    return activities


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific activity by ID."""
    from app.models.activity import Activity

    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Activity not found")

    return activity
