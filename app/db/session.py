from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    settings.postgres.user,
    settings.postgres.password,
    settings.postgres.host,
    settings.postgres.port,
    settings.postgres.database,
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=settings.service.debug, pool_pre_ping=True
)
Session = sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
