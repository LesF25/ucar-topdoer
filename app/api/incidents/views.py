from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Incident
from ..dependencies import get_db_session
from .dependencies import get_incident_by_id
from .schemas import (
    IncidentCreateRequest,
    IncidentResponse,
    IncidentUpdatePartialRequest,
    IncidentGetRequest,
)
from . import crud

router = APIRouter(
    prefix='/incidents',
    tags=['incidents'],
)


@router.post(
    path='/',
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_incident(
    dto: IncidentCreateRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await crud.create_incident(session, dto)


@router.get(
    path='/',
    response_model=list[IncidentResponse]
)
async def get_incidents(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    dto: Annotated[IncidentGetRequest, Query()],
):
    return await crud.get_incidents(session, dto)


@router.patch(
    path='/{incident_id}',
    response_model=IncidentResponse,
)
async def update_incident_status(
    dto: IncidentUpdatePartialRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    incident: Annotated[Incident, Depends(get_incident_by_id)],
):
    return await crud.update_incident(
        session=session,
        incident=incident,
        dto=dto,
    )
