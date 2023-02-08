from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config.settings import BackendSettings, settings


class AsyncPostgres:
    """
    Async PostgreSQL connection manager.
    """

    def __init__(self, backend_settings: BackendSettings) -> None:
        self._postgres_url = (
            "postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}".format(
                username=backend_settings.POSTGRES_USERNAME,
                password=backend_settings.POSTGRES_PASSWORD,
                host=backend_settings.POSTGRES_HOST,
                port=backend_settings.POSTGRES_PORT,
                db_name=backend_settings.POSTGRES_NAME,
            )
        )

        self._async_engine = create_async_engine(
            url=self._postgres_url,
            echo=backend_settings.IS_POSTGRES_ECHO_LOG,
            pool_pre_ping=True,
        )
        self._async_session = async_sessionmaker(
            bind=self._async_engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=backend_settings.IS_POSTGRES_SESSION_EXPIRE_ON_COMMIT,
        )

    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        return self._async_session


async_postgres = AsyncPostgres(backend_settings=settings)
