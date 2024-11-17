from sqlalchemy import MetaData, Table

from data_forge.core.models import Source


class SqlBuilder:
    @classmethod
    def build_query_from_source(cls, source: Source, metadata: MetaData):
        pass

    @staticmethod
    def get_table(table_name: str, metadata: MetaData) -> Table:
        return Table(table_name, metadata)
