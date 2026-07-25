# Activity Log model for tracking user and system actions

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.enums import ActivityType, ActivityLevel


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    activity_type: Mapped[ActivityType] = mapped_column(
        SQLEnum(ActivityType),
        nullable=False,
    )

    level: Mapped[ActivityLevel] = mapped_column(
        SQLEnum(ActivityLevel),
        nullable=False,
        default=ActivityLevel.INFO,
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    device_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    device_hostname: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    user: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
