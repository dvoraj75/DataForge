from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from data_forge.settings import PostgresDbSettings


class Database:
    def __init__(self, config: PostgresDbSettings):
        self.engine = create_async_engine(
            config.dsn,
            **config.model_dump()
        )

        self.async_session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    def get_session(self) -> AsyncSession:
        return self.async_session_factory()
