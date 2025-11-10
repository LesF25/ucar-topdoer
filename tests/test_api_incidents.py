from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete

from app.api.incidents.schemas import IncidentCreateRequest, IncidentResponse
from app.core.structures import IncidentSource, IncidentStatus
from app.core.db import DatabaseSessionManager
from app.models.incident import Incident
from app.api.incidents import crud


@pytest_asyncio.fixture
async def clean_incident_table(
    f_database_session_manager: DatabaseSessionManager,
) -> AsyncIterator[None]:
    yield
    async with f_database_session_manager.session() as session:
        await session.execute(delete(Incident))
        await session.commit()


@pytest.fixture
def f_incident_create() -> IncidentCreateRequest:
    return IncidentCreateRequest(
        description='Scooter offline',
        source=IncidentSource.OPERATOR,
    )

@pytest.mark.usefixtures('clean_incident_table')
@pytest.mark.asyncio
async def test_create_incident_endpoint(
    f_incident_create: IncidentCreateRequest,
    f_client: AsyncClient,
):
    response = await f_client.post(
        '/api/incidents/',
        json=f_incident_create.model_dump(),
    )
    assert response.status_code == 201

    response = response.json()
    assert response['description'] == f_incident_create.description
    assert response['source'] == IncidentSource.OPERATOR.value
    assert response['status'] == IncidentStatus.OPEN.value


@pytest.mark.usefixtures('clean_incident_table')
@pytest.mark.asyncio
async def test_update_incident_endpoint_with_raise_404(
    f_client: AsyncClient,
    f_incident_create: IncidentCreateRequest,
):
    fake_incident_id = 12345
    not_found_response = await f_client.patch(
        f'/api/incidents/{fake_incident_id}',
        json={'status': IncidentStatus.CLOSED.value},
    )
    assert not_found_response.status_code == 404


@pytest.mark.usefixtures('clean_incident_table')
@pytest.mark.asyncio
async def test_update_incident_endpoint(
    f_client: AsyncClient,
    f_incident_create: IncidentCreateRequest,
    f_database_session_manager: DatabaseSessionManager,
):
    async with f_database_session_manager.session() as session:
        incident = await crud.create_incident(session, f_incident_create)
        incident = IncidentResponse.model_validate(incident)

    update_response = await f_client.patch(
        f'/api/incidents/{incident.id}',
        json={'status': IncidentStatus.RESOLVED.value},
    )
    assert update_response.status_code == 200

    update_response = update_response.json()
    assert update_response['status'] == IncidentStatus.RESOLVED.value


@pytest.mark.usefixtures('clean_incident_table')
@pytest.mark.asyncio
async def test_get_incident_endpoint_without_filters(
    f_client: AsyncClient,
    f_incident_create: IncidentCreateRequest,
    f_database_session_manager: DatabaseSessionManager,
):
    async with f_database_session_manager.session() as session:
        incident = await crud.create_incident(session, f_incident_create)
        incident = IncidentResponse.model_validate(incident)

    response = await f_client.get('/api/incidents/')
    assert response.status_code == 200
    assert response.json() == [
        incident.model_dump(mode='json')
    ]


@pytest.mark.usefixtures('clean_incident_table')
@pytest.mark.asyncio
async def test_get_incident_endpoint_with_filters(
    f_client: AsyncClient,
    f_incident_create: IncidentCreateRequest,
    f_database_session_manager: DatabaseSessionManager,
):
    async with f_database_session_manager.session() as session:
        incident = await crud.create_incident(session, f_incident_create)
        incident = IncidentResponse.model_validate(incident)

    response = await f_client.get(
        '/api/incidents/',
        params={'statuses': [IncidentStatus.OPEN.value]}
    )
    assert response.status_code == 200
    assert response.json() == [
        incident.model_dump(mode='json')
    ]

    response = await f_client.get(
        '/api/incidents/',
        params={'statuses': [IncidentStatus.RESOLVED.value]}
    )
    assert response.status_code == 200
    assert response.json() == []
