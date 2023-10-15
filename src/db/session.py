from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings


class AsyncPostgres:
    """
    Async PostgreSQL connection manager.
    """

    def __init__(self) -> None:
        self._engine = create_async_engine(
            url=settings.POSTGRES_URL,
            pool_pre_ping=True,
        )

        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
        )
        self._session = self._sessionmaker()

    async def __aenter__(self) -> AsyncSession:
        """
        Asynchronous Connection Session.
        """
        return await self._session.__aenter__()

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self._session.__aexit__(*args, **kwargs)
