from enum import StrEnum


class JobTriggerType(StrEnum):
    INTERVAL = "interval"
    CRON = "cron"
    DATE = "date"


class OutputFormat(StrEnum):
    PDF = "pdf"
    CSV = "csv"
    HTML = "html"


class Operator(StrEnum):
    EQ = "="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    BETWEEN = "BETWEEN"
    NOT_BETWEEN = "NOT BETWEEN"
    IN = "IN"
    NOT_IN = "NOT IN"
    LIKE = "LIKE"
    NOT_LIKE = "NOT LIKE"
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"


class Order(StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class OperationType(StrEnum):
    AGGREGATE = "aggregate"
    SORT = "sort"
    FILTER = "filter"
    LIMIT = "limit"
    JOIN = "join"
    COMPUTE = "compute"
    GROUP_BY = "group_by"
    DISTINCT = "distinct"


class CalculationType(StrEnum):
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    COUNT = "count"


class OutputType(StrEnum):
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    FILESYSTEM = "filesystem"
    SSH = "ssh"
    SFTP = "sftp"
    FTP = "ftp"
