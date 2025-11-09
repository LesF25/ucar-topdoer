from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import database_session_manager


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with database_session_manager.session() as session:
        yield session
