from typing import Optional
from urllib.parse import quote_plus

from pydantic import Field, PositiveInt, computed_field
from pydantic_settings import BaseSettings


class PostgresDbSettings(BaseSettings):
    username: str
    password: str
    host: str
    port: PositiveInt = Field(default=5432)
    db: str
    db_schema: str = Field(default="Public")
    pool_size: PositiveInt = Field(default=5)
    max_overflow: PositiveInt = Field(default=10)
    pool_timeout: PositiveInt = Field(default=30)
    application_name: str = Field(default="DataForge")

    class Config:
        env_prefix = "POSTGRES_"

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{quote_plus(self.username)}:{quote_plus(self.password)}@{self.host}:{self.port}/{self.db}"

    @computed_field
    def connect_args(self) -> dict[str, dict[str, str]]:
        return {"server_settings": {"application_name": self.application_name, "search_path": self.db_schema}}


class LoggingSettings(BaseSettings):
    config_path: str

    class Config:
        env_prefix = "LOGGING_"


class SentrySettings(BaseSettings):
    dsn: str
    environment: str

    class Config:
        env_prefix = "SENTRY_"


class AppSettings(BaseSettings):
    postgres: PostgresDbSettings
    logging: Optional[LoggingSettings]
    sentry: Optional[SentrySettings]
