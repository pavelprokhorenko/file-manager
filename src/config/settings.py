from pathlib import Path

from decouple import Csv, config
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()


class BackendSettings(BaseSettings):
    """
    Base settings for all backend.
    """

    # Base
    TITLE: str = config("TITLE", cast=str)
    VERSION: str = config("VERSION", cast=str)
    DEBUG: bool = config("DEBUG", cast=bool)

    # Server
    SERVER_HOST: str = config("SERVER_HOST", cast=str)
    SERVER_PORT: int = config("SERVER_PORT", cast=int)
    SERVER_WORKERS: int = config("SERVER_WORKERS", cast=int)

    ALLOWED_ORIGINS: list[str] = config("ALLOWED_ORIGINS", cast=Csv())
    ALLOWED_METHODS: list[str] = config("ALLOWED_METHODS", cast=Csv())
    ALLOWED_HEADERS: list[str] = config("ALLOWED_HEADERS", cast=Csv())

    # Postgres
    POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str)
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int)
    POSTGRES_DB: str = config("POSTGRES_DB", cast=str)
    POSTGRES_USERNAME: str = config("POSTGRES_USERNAME", cast=str)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str)
    POSTGRES_URL: str = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(  # noqa: FS002
        user=POSTGRES_USERNAME,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db=POSTGRES_DB,
    )

    model_config = SettingsConfigDict(
        env_file=f"{ROOT_DIR}/.env",
        case_sensitive=True,
        validate_assignment=True,
    )


settings = BackendSettings()
