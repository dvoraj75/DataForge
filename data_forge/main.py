from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from data_forge.api import v1_router
from data_forge.core.scheduler import DataForgeScheduler


@asynccontextmanager
async def life_span(app: FastAPI) -> None:  # noqa: RUF029
    app.state.scheduler.start()
    yield
    app.state.scheduler.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=life_span)
    app.state.scheduler = DataForgeScheduler.init_scheduler()
    app.include_router(v1_router)
    return app