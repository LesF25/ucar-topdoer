from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Incident
from .schemas import IncidentCreateRequest, IncidentUpdatePartialRequest
from app.core.structures import IncidentStatus


async def create_incident(
    session: AsyncSession,
    dto: IncidentCreateRequest,
) -> Incident:
    incident = Incident(**dto.model_dump())

    session.add(incident)
    await session.commit()

    return incident


async def get_incidents(
    session: AsyncSession,
    statuses: list[IncidentStatus] | None = None,
) -> list[Incident]:
    statement = select(Incident)

    if statuses:
        statement = statement.where(
            Incident.status.in_(statuses)
        )

    result: Result = await session.execute(statement=statement)
    incidents = result.scalars().all()

    return list(incidents)


async def update_incident(
    session: AsyncSession,
    incident: Incident,
    dto: IncidentUpdatePartialRequest,
) -> Incident:
    for key, val in dto.model_dump().items():
        setattr(incident, key, val)

    await session.commit()
    return incident


async def get_incident_by_id(
    session: AsyncSession,
    incident_id: int,
) -> Incident | None:
    return await session.get(Incident, incident_id)
