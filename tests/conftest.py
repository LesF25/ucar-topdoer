from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from app.core.db import DatabaseSessionManager, database_session_manager
from app.models.base import Base
from app.main import app


@pytest_asyncio.fixture
async def f_engine() -> AsyncEngine:
    engine = create_async_engine(
        str(settings.database.url),
        echo=settings.database.echo,
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
def f_database_session_manager(
    f_engine: AsyncEngine,
    monkeypatch: pytest.MonkeyPatch,
) -> DatabaseSessionManager:
    session_factory = async_sessionmaker(
        bind=f_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    monkeypatch.setattr(
        database_session_manager,
        '_engine',
        f_engine,
    )
    monkeypatch.setattr(
        database_session_manager,
        '_session_factory',
        session_factory,
    )

    return database_session_manager


@pytest_asyncio.fixture
@pytest.mark.usefixtures('f_database_session_manager')
async def f_client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://testserver',
    ) as async_client:
        yield async_client
