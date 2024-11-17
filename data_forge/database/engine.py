from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from data_forge.settings import PostgresDbSettings


class Database:
    def __init__(self, config: PostgresDbSettings) -> None:
        self.engine = create_async_engine(config.dsn, **config.model_dump())

        self.async_session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

        self.metadata = MetaData()

    # def get_session(self) -> AsyncSession:
    #     return self.async_session_factory()

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.async_session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    async def reflect_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.reflect)
