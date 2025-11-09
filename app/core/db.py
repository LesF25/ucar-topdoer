from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from ..config import settings


class DatabaseSessionManager:
    def __init__(
        self,
        url: str,
        echo: bool = False,
    ):
        self._engine = create_async_engine(url=url, echo=echo)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def session(self):
        async with self._session_factory() as session:
            yield session


database_session_manager = DatabaseSessionManager(
    url=str(settings.database.url),
    echo=settings.database.echo,
)
