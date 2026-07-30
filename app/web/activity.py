# Activity web routes
from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.services.activity_service import activity_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/activities")
def list_activities(
    request: Request,
    limit: int = Query(default=50, le=100),
    activity_type: Optional[str] = Query(default=None, description="Filter by activity type"),
    level: Optional[str] = Query(default=None, description="Filter by level"),
    db: Session = Depends(get_db),
):
    """Display activity log page."""
    from app.models.enums import ActivityType, ActivityLevel

    at = ActivityType(activity_type) if activity_type else None
    lvl = ActivityLevel(level) if level else None

    activities = activity_service.get_recent_activities(
        db=db,
        limit=limit,
        activity_type=at,
        level=lvl,
    )

    return templates.TemplateResponse(
        request=request,
        name="activity/logs.html",
        context={
            "request": request,
            "activities": activities,
            "activity_types": ActivityType,
            "levels": ActivityLevel,
            "selected_type": activity_type,
            "selected_level": level,
            "active_page": "activities",
        },
    )
