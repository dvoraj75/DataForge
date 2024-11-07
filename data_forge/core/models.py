import logging
from datetime import datetime
from typing import Optional, Self, TypeAlias, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from data_forge.core.enums import CalculationType, JobType, OperationType, Operator, Order, OutputFormat, OutputType
from data_forge.core.exceptions import InvalidJobConfigurationError

logger = logging.getLogger(__name__)


OperationConfig: TypeAlias = Union[
    "AggregateConfig",
    "SortConfig",
    "FilterConfig",
    "LimitConfig",
    "JoinConfig",
    "ComputeConfig",
    "GroupByConfig",
    "DistinctConfig",
]

OutputConfig: TypeAlias = Union[
    "EmailConfig",
    "SlackConfig",
    "TeamsConfig",
    "FilesystemConfig",
    "SSHConfig",
    "SFTPConfig",
    "FTPConfig",
]


class EmailConfig(BaseModel):
    subject: Optional[str]
    body: Optional[str]
    from_address: Optional[str]
    to_address: Optional[str]


class SlackConfig(BaseModel):
    pass


class TeamsConfig(BaseModel):
    pass


class FilesystemConfig(BaseModel):
    destination: str


class SSHConfig(BaseModel):
    pass


class SFTPConfig(BaseModel):
    pass


class FTPConfig(BaseModel):
    pass


class Output(BaseModel):
    filename: str
    format: OutputFormat
    type: OutputType
    config: OutputConfig


class CalculationConfig(BaseModel):
    type: CalculationType
    column: str


class AggregateConfig(BaseModel):
    by: list[str] = Field(default_factory=list)
    calculations: list[CalculationConfig]


class SortConfig(BaseModel):
    by: list[str] = Field(default_factory=list)
    order: Order = Order.ASC


class LimitConfig(BaseModel):
    count: int


class JoinConfig(BaseModel):
    table_name: str
    on: str
    columns: list[str] = Field(default_factory=list)


class ComputeConfig(BaseModel):
    new_column: str
    expression: str


class GroupByConfig(BaseModel):
    by: list[str] = Field(default_factory=list)


class DistinctConfig(BaseModel):
    columns: list[str] = Field(default_factory=list)


class FilterConfig(BaseModel):
    field_name: str
    operator: Operator
    value: str


class Operation(BaseModel):
    type: OperationType
    config: OperationConfig


class Source(BaseModel):
    db_table_name: str
    columns: list[str] = Field(default_factory=list)
    filters: list[FilterConfig] = Field(default_factory=list)
    operations: list[Operation] = Field(default_factory=list)


class Table(BaseModel):
    name: str = Field("")
    source: Source


class Report(BaseModel):
    name: str = Field("")
    tables: list[Table]
    outputs: list[Output]


class CronConfig(BaseModel):
    year: Optional[int] = Field(None, ge=2024)
    month: Optional[int] = Field(None, ge=1, le=12)
    day: Optional[int] = Field(None, ge=1, le=31)
    week: Optional[int] = Field(None, ge=1, le=52)
    day_of_week: Optional[int] = Field(None, ge=0, le=7)
    second: Optional[int] = Field(None, ge=0, le=59)
    minute: Optional[int] = Field(None, ge=0, le=59)
    hour: Optional[int] = Field(None, ge=0, le=23)


class DateConfig(BaseModel):
    run_date: datetime


class IntervalConfig(BaseModel):
    seconds: Optional[int] = Field(None, ge=0, le=59)
    minutes: Optional[int] = Field(None, ge=0, le=59)
    hours: Optional[int] = Field(None, ge=0, le=23)


class Job(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    job_type: JobType
    job_config: IntervalConfig | DateConfig | CronConfig
    reports: list[Report] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_job_type(self) -> Self:
        match self.job_type:
            case JobType.INTERVAL:
                if isinstance(self.job_config, IntervalConfig):
                    return self
            case JobType.CRON:
                if isinstance(self.job_config, CronConfig):
                    return self
            case JobType.DATE:
                if isinstance(self.job_config, DateConfig):
                    return self
            case _:
                logger.error("Unknonw job type '%s'", self.job_type)
                raise InvalidJobConfigurationError(f"Unknown job type: {self.job_type}")
        logger.error("Invalid configuration type '%s' for job type '%s'", type(self.job_config), self.job_type)
        raise InvalidJobConfigurationError(f"Invalid configuration type for job '{self.job_type}'")
