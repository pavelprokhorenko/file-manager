from pathlib import Path

from pydantic import BaseSettings
from yaml import SafeLoader, load

CONFIG_FILE = f"{Path(__file__).parent.absolute()}/settings.yaml"


class Postgres(BaseSettings):
    """
    Settings for postgres db.
    """

    host: str
    port: int
    user: str
    password: str
    database: str
    test_database: str


class Service(BaseSettings):
    """
    Settings for service.
    """

    host: str
    port: int
    debug: bool
    origins: list[str]


class GraphQL(BaseSettings):
    """
    Settings for GraphQL.
    """

    endpoint: str


class Settings(BaseSettings):
    postgres: Postgres
    service: Service
    graphql: GraphQL


def setup_settings() -> Settings:
    """
    Setup settings from config file.
    """
    with open(CONFIG_FILE) as f:
        config = load(f, SafeLoader)
        return Settings.parse_obj(config)


settings = setup_settings()
