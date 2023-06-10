from pathlib import Path

from decouple import config
from pydantic import BaseConfig, BaseSettings

ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()


class BackendSettings(BaseSettings):
    """
    Base settings for all backend of service.
    """

    # Base
    TITLE: str = "AWS File Manager"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Server
    SERVER_HOST: str = config("BACKEND_SERVER_HOST", cast=str)
    SERVER_PORT: int = config("BACKEND_SERVER_PORT", cast=int)
    SERVER_WORKERS: int = config("BACKEND_SERVER_WORKERS", cast=int)
    API_GRAPHQL_PREFIX: str = "/graphql"

    ALLOWED_ORIGINS: list[str]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    # Postgres
    POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str)
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int)
    POSTGRES_NAME: str = config("POSTGRES_DB", cast=str)
    POSTGRES_USERNAME: str = config("POSTGRES_USERNAME", cast=str)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str)

    IS_POSTGRES_ECHO_LOG: bool = config("IS_POSTGRES_ECHO_LOG", cast=bool)
    IS_POSTGRES_SESSION_EXPIRE_ON_COMMIT: bool = config("IS_POSTGRES_SESSION_EXPIRE_ON_COMMIT", cast=bool)

    class Config(BaseConfig):
        env_file = f"{ROOT_DIR}/.env"
        case_sensitive: bool = True
        validate_assignment: bool = True


settings = BackendSettings()
