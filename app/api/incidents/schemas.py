from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.structures import IncidentSource, IncidentStatus


class IncidentBase(BaseModel):
    description: str = Field(
        min_length=1,
        max_length=4096,
    )
    source: IncidentSource = Field(
        default=IncidentSource.MONITORING
    )


class IncidentCreateRequest(IncidentBase):
    ...


class IncidentResponse(IncidentBase):
    id: int
    status: IncidentStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentUpdatePartialRequest(BaseModel):
    status: IncidentStatus


class IncidentGetRequest(BaseModel):
    statuses: list[IncidentStatus] | None = None
