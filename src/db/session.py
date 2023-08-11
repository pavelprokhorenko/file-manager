from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config.settings import settings


class AsyncPostgres:
    """
    Async PostgreSQL connection manager.
    """

    def __init__(self) -> None:
        self._url = settings.POSTGRES_URL

        self._engine = create_async_engine(
            url=self._url,
            pool_pre_ping=True,
        )

        self._session = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
        )

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        """
        Asynchronous Connection Session.
        """

        return self._session

    @property
    def url(self) -> str:
        """
        Connection URL.
        """

        return self._url


async_postgres = AsyncPostgres()
