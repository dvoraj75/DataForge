from contextlib import asynccontextmanager

from fastapi import FastAPI

from data_forge.api import v1_router
from data_forge.api.handlers import invalid_job_configration_exception_handler
from data_forge.core.exceptions import InvalidJobConfigurationError
from data_forge.core.scheduler import DataForgeScheduler


@asynccontextmanager
async def life_span(app: FastAPI) -> None:  # noqa: RUF029
    app.state.scheduler.start()
    yield
    app.state.scheduler.shutdown()


def init_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidJobConfigurationError, invalid_job_configration_exception_handler)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=life_span)
    app.state.scheduler = DataForgeScheduler.init_scheduler()
    app.include_router(v1_router)
    init_handlers(app)
    return app
