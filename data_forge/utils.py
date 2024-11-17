from typing import Type

from pydantic_core import ValidationError
from pydantic_settings import BaseSettings

from data_forge.settings import AppSettings, LoggingSettings, PostgresDbSettings, SentrySettings


def get_app_settings() -> AppSettings:
    return AppSettings(
        postgres=PostgresDbSettings(),
        logging=get_instance_or_none(LoggingSettings),
        sentry=get_instance_or_none(SentrySettings),
    )


def get_instance_or_none(klass: Type[BaseSettings]) -> BaseSettings | None:
    try:
        return klass()
    except ValidationError:
        return None
