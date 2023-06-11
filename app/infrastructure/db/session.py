from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.settings import BackendSettings, settings


class AsyncPostgres:
    """
    Async PostgreSQL connection manager.
    """

    def __init__(self, backend_settings: BackendSettings) -> None:
        self._url = backend_settings.POSTGRES_URL
        self._engine = create_async_engine(
            url=self._url,
            echo=backend_settings.IS_POSTGRES_ECHO_LOG,
            pool_pre_ping=True,
        )
        self._session = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=backend_settings.IS_POSTGRES_SESSION_EXPIRE_ON_COMMIT,
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


async_postgres = AsyncPostgres(backend_settings=settings)
