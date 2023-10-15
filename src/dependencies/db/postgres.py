from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import AsyncPostgres


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Establish connection to database.
    After closing HTTP session disconnect from database.
    """

    async with AsyncPostgres() as session:
        yield session
        await session.commit()
