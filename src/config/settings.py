from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

from decouple import Csv, config
from pydantic import BaseConfig, BaseSettings, PostgresDsn, root_validator

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
    SERVER_HOST: str = config("BACKEND_SERVER_HOST", cast=str)
    SERVER_PORT: int = config("BACKEND_SERVER_PORT", cast=int)
    SERVER_WORKERS: int = config("BACKEND_SERVER_WORKERS", cast=int)

    ALLOWED_ORIGINS: list[str] = config("ALLOWED_ORIGINS", cast=Csv())
    ALLOWED_METHODS: list[str] = config("ALLOWED_METHODS", cast=Csv())
    ALLOWED_HEADERS: list[str] = config("ALLOWED_HEADERS", cast=Csv())

    # Postgres
    POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str)
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int)
    POSTGRES_DB: str = config("POSTGRES_DB", cast=str)
    POSTGRES_USERNAME: str = config("POSTGRES_USERNAME", cast=str)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str)
    POSTGRES_URL: str = config("POSTGRES_URL", cast=str)

    @root_validator(pre=True)
    def assemble_postgres_db_url(cls, values: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        postgres_url = values.get("POSTGRES_URL")
        if not postgres_url or not isinstance(postgres_url, str):
            values["POSTGRES_URL"] = str(
                PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    user=values["POSTGRES_USERNAME"],
                    password=values["POSTGRES_PASSWORD"],
                    host=values["POSTGRES_HOST"],
                    port=str(values["POSTGRES_PORT"]),
                    path=f'/{values["POSTGRES_DB"]}',
                )
            )
        return values

    class Config(BaseConfig):
        env_file = f"{ROOT_DIR}/.env"
        case_sensitive: bool = True
        validate_assignment: bool = True


settings = BackendSettings()
