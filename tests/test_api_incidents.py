from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete

from app.core.structures import IncidentSource, IncidentStatus
from app.core.db import DatabaseSessionManager
from app.models.incident import Incident


@pytest_asyncio.fixture(autouse=True)
async def _clean_database(
    f_database_session_manager: DatabaseSessionManager,
) -> AsyncIterator[None]:
    yield
    async with f_database_session_manager.session() as session:
        await session.execute(delete(Incident))
        await session.commit()


async def create_incident_via_api(
    client: AsyncClient,
    payload: dict
) -> dict:
    response = await client.post('/api/incidents/', json=payload)
    assert response.status_code == 201
    return response.json()


@pytest.mark.asyncio
async def test_create_incident_endpoint(f_client: AsyncClient):
    payload = {
        'description': 'Scooter offline',
        'source': IncidentSource.OPERATOR.value,
    }
    response = await create_incident_via_api(
        f_client,
        payload,
    )

    assert response['description'] == payload['description']
    assert response['source'] == IncidentSource.OPERATOR.value
    assert response['status'] == IncidentStatus.OPEN.value


@pytest.mark.asyncio
async def test_all_incident_endpoint(
    f_client: AsyncClient,
):
    create_response_1 = await create_incident_via_api(
        f_client,
        {'description': 'Ops alert', 'source': IncidentSource.MONITORING.value},
    )
    create_response_2 = await create_incident_via_api(
        f_client,
        {'description': 'Partner report', 'source': IncidentSource.PARTNER.value},
    )

    get_incidents_response_before_update = await f_client.get('/api/incidents/')
    assert get_incidents_response_before_update.json() == [
        create_response_1,
        create_response_2,
    ]

    not_found_response = await f_client.patch(
        '/api/incidents/9999',
        json={'status': IncidentStatus.CLOSED.value},
    )
    assert not_found_response.status_code == 404

    update_response = await f_client.patch(
        f'/api/incidents/{create_response_1['id']}',
        json={'status': IncidentStatus.RESOLVED.value},
    )
    assert update_response.status_code == 200

    create_response_1 = {
        **create_response_1,
        'status': IncidentStatus.RESOLVED.value,
    }
    assert update_response.json() == create_response_1

    get_incidents_response_after_update = await f_client.get('/api/incidents/')
    assert get_incidents_response_after_update.status_code == 200
    assert get_incidents_response_after_update.json() == [
        create_response_2,
        create_response_1,
    ]

    filtered_response = await f_client.get(
        '/api/incidents/',
        params={'statuses': [IncidentStatus.RESOLVED.value]},
    )
    assert filtered_response.status_code == 200
    assert filtered_response.json() == [create_response_1]
