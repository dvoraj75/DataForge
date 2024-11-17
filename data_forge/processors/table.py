import logging

from data_forge.core.models import Source, TableConfig
from data_forge.database.builder import SqlBuilder
from data_forge.database.engine import Database
from data_forge.processors.models import Table

logger = logging.getLogger(__name__)


class TableProcessor:
    def __init__(self, db: Database, builder: SqlBuilder) -> None:
        self.db = db
        self.builder = builder

    async def generate_table(self, table_config: TableConfig) -> Table:
        logger.info("Generating table '%s'", table_config.name)
        await self.db.reflect_db()
        query = self.build_query(table_config.source)

    def build_query(self, source: Source):
        return self.builder.build_query_from_source(source, self.db.metadata)
