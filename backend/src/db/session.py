from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    settings.POSTGRES_USERNAME,
    settings.POSTGRES_PASSWORD,
    settings.POSTGRES_HOST,
    settings.POSTGRES_PORT,
    settings.POSTGRES_NAME,
)

engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL, echo=settings.IS_POSTGRES_ECHO_LOG, pool_pre_ping=True
)
Session = sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=settings.IS_POSTGRES_SESSION_EXPIRE_ON_COMMIT,
)
