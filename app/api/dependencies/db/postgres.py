from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import async_postgres


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Connect to database. After closing HTTP session disconnect from database.
    """
    async with async_postgres.session() as session:
        yield session
