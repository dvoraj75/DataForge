import logging

from data_forge.core.models import Report
from data_forge.processors import TableProcessor

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self, table_processor: TableProcessor) -> None:
        self.table_processor = table_processor

    async def generate_report(self, report_config: Report) -> None:
        logger.info("Generating report '%s' from config", report_config.name)
        tables = [await self.table_processor.generate_table(table_config) for table_config in report_config.tables]
        print(tables)
