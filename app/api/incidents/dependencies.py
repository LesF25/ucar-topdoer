from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Incident
from ..dependencies import get_db_session
from . import crud


async def get_incident_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    incident_id: Annotated[int, Path(ge=1)],
) -> Incident:
    incident = await crud.get_incident_by_id(
        session=session,
        incident_id=incident_id,
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Incident {incident_id} not found.'
        )

    return incident
