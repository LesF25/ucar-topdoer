from datetime import datetime

from sqlalchemy import Enum, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.structures import IncidentStatus, IncidentSource
from .base import Base


class Incident(Base):
    __tablename__ = 'incidents'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(
            IncidentStatus,
            name='incident_status',
            native_enum=False,
        ),
        default=IncidentStatus.OPEN,
        nullable=False,
    )
    source: Mapped[IncidentSource] = mapped_column(
        Enum(
            IncidentSource,
            name='incident_source',
            native_enum=False,
        ),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(),
        server_default=func.now(),
        nullable=False,
    )
