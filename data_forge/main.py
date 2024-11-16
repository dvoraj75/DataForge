import json
import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration

from data_forge.api import v1_router
from data_forge.api.handlers import invalid_configration_exception_handler, job_does_not_exist_error_handler
from data_forge.core.exceptions import InvalidJobConfigurationError, JobDoesNotExistError
from data_forge.core.scheduler import DataForgeScheduler
from data_forge.settings import LoggingSettings, SentrySettings
from data_forge.utils import get_app_settings


@asynccontextmanager
async def life_span(app: FastAPI) -> None:  # noqa: RUF029
    app.state.scheduler.start()
    yield
    app.state.scheduler.shutdown()


def init_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidJobConfigurationError, invalid_configration_exception_handler)
    app.add_exception_handler(JobDoesNotExistError, job_does_not_exist_error_handler)


def init_logging(settings: Optional[LoggingSettings]) -> None:
    if settings is None:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            handlers=[logging.StreamHandler()],  # logy do konzole
        )
        logging.info("Logging initialized")
        return

    with open(settings.config_path) as f:
        log_config = json.load(f)
    logging.config.dictConfig(log_config)


def init_sentry(settings: SentrySettings) -> None:
    sentry_sdk.init(
        dsn=settings.dsn,
        environment=settings.environment,
        traces_sample_rate=0.2,
        profiles_sample_rate=0.2,
        integrations=[AsyncioIntegration(),],
    )


def create_app() -> FastAPI:
    app_settings = get_app_settings()
    app = FastAPI(lifespan=life_span)

    init_handlers(app)
    init_logging(app_settings.logging)

    if app_settings.sentry:
        init_sentry(app_settings.sentry)

    app.state.scheduler = DataForgeScheduler.init_scheduler()
    app.include_router(v1_router)

    logging.info("Application initialized")
    return app
