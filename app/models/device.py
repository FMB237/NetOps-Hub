# File that will contain all our devices settings 

import uuid # Our device wil all have uuids 
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# Here we are mainly entrying the DB Importations
from app.database.base import Base
from app.models.enums import DeviceType
from app.models.enums import Vendor


class Device(Base):
    __tablename__ = "devices"

    id : Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    hostname : Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    ip_address : Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        unique=True,
    )
    model : Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    vendor: Mapped[Vendor] = mapped_column(
        Enum(Vendor),
        nullable=False,
    )
    device_type : Mapped[DeviceType] = mapped_column(
        Enum(DeviceType),
        nullable=False,
    )
    operating_system : Mapped[str]  = mapped_column(
        String(100),
        nullable=False,
    )
    ssh_port : Mapped[Integer] = mapped_column(
        Integer,
        default=22,
    ) 
    username : Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    location : Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    notes : Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at : Mapped [datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    ) 
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )