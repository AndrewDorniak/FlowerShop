from functools import lru_cache

from pydantic import BaseSettings

from src.core.settings.uvicorn import UvicornSettings
from src.core.settings.postgres import PostgreSQLSettings
from src.core.settings.sqlalchemy import SqlAlchemySettings
from src.core.settings.auth import AuthSettings


class Settings(BaseSettings):
    """Deposit Service API settings."""

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

    api_prefix: str = ""
    root_path: str = ""
    app_version: str = "latest"
    project_name: str
    app_slug: str

    debug: bool | None

    uvicorn: UvicornSettings = UvicornSettings()
    postgres: PostgreSQLSettings = PostgreSQLSettings()
    sqlalchemy: SqlAlchemySettings = SqlAlchemySettings()
    auth: AuthSettings = AuthSettings()


@lru_cache
def get_settings():
    """Получение и кэширование настроек проекта."""
    settings = Settings()
    return settings


settings = get_settings()