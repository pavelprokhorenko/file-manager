from collections.abc import AsyncGenerator

import alembic
import alembic.command
import alembic.config
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from src.config import settings
from src.core.tests.utils import upgrade_database


@pytest.fixture(
    scope="session",
    autouse=True,
)
def _mock_postgres_url() -> None:
    settings.POSTGRES_URL = settings.POSTGRES_TEST_URL


@pytest_asyncio.fixture(scope="session")
async def connection() -> AsyncGenerator[AsyncConnection, None]:
    """
    Set up database connection.
    """

    engine = create_async_engine(
        url=settings.POSTGRES_TEST_URL,
        pool_pre_ping=True,
    )

    async with engine.connect() as conn:
        yield conn


@pytest_asyncio.fixture(scope="session")
async def alembic_config() -> alembic.config.Config:
    """
    Alembic config generated from context.
    """
    config = alembic.config.Config(
        settings.ROOT_DIR / "alembic.ini",
    )

    config.set_main_option(
        "sqlalchemy.url",
        settings.POSTGRES_TEST_URL,
    )
    return config


@pytest_asyncio.fixture(
    scope="session",
    autouse=True,
)
async def _migrate_database(
    connection: AsyncConnection,
    alembic_config: alembic.config.Config,
) -> None:
    """
    Migrate database to latest revision.
    """

    await connection.run_sync(upgrade_database, alembic_config)


@pytest_asyncio.fixture(autouse=True)
@pytest.mark.usefixtures(  # noqa: PT025
    # used for application order
    "_migrate_database",
)
async def _pg_transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[None, None]:
    """
    Wrap each test in a 100% rollback transaction.
    """

    transaction = connection
    await transaction.begin()

    yield

    await transaction.rollback()
