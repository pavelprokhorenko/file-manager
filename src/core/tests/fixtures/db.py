from collections.abc import AsyncGenerator

import alembic
import alembic.command
import alembic.config
import pytest
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from src.config import settings


@pytest.fixture(scope="session")
def alembic_config() -> alembic.config.Config:
    """
    Alembic config generated from context.
    """

    return alembic.config.Config(
        settings.ROOT_DIR / "alembic.ini",
    )


@pytest.fixture(
    scope="session",
    autouse=True,
)
def _migrate_database(
    alembic_config: alembic.config.Config,
) -> None:
    """
    Migrate database to latest revision.
    """

    alembic.command.upgrade(
        config=alembic_config,
        revision="head",
    )


@pytest.fixture(scope="session")
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


@pytest.fixture(autouse=True)
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
