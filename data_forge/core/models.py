import logging
from datetime import datetime
from typing import Any, Optional, TypeAlias, Union
from uuid import UUID, uuid4

from apscheduler.job import Job as SchedulerJob
from pydantic import BaseModel, Field, model_validator

from data_forge.core.enums import (
    CalculationType,
    JobTriggerType,
    OperationType,
    Operator,
    Order,
    OutputFormat,
    OutputType,
)
from data_forge.core.exceptions import InvalidJobConfigurationError
from data_forge.core.triggers import CustomCronTrigger, CustomDateTrigger, CustomIntervalTrigger, JobTrigger

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

JobTriggerConfig: TypeAlias = Union[
    "IntervalConfig",
    "CronConfig",
    "DateConfig",
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
    year: Optional[str] = Field(None, ge=2024)
    month: Optional[str] = Field(None, ge=1, le=12)
    day: Optional[str] = Field(None, ge=1, le=31)
    week: Optional[str] = Field(None, ge=1, le=52)
    day_of_week: Optional[str] = Field(None, ge=0, le=7)
    second: Optional[str] = Field(None, ge=0, le=59)
    minute: Optional[str] = Field(None, ge=0, le=59)
    hour: Optional[str] = Field(None, ge=0, le=23)


class DateConfig(BaseModel):
    run_date: datetime


class IntervalConfig(BaseModel):
    seconds: Optional[int] = Field(None, ge=0)
    minutes: Optional[int] = Field(None, ge=0)
    hours: Optional[int] = Field(None, ge=0)
    days: Optional[int] = Field(None, ge=0)
    weeks: Optional[int] = Field(None, ge=0)


class Job(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: Optional[str] = None
    job_trigger_type: JobTriggerType
    job_trigger_config: JobTriggerConfig
    reports: list[Report] = Field(min_length=1)

    @classmethod
    def from_scheduler_job(cls, job: SchedulerJob) -> "Job":
        job_type, job_config = cls.get_trigger_info_from_scheduler_job(job.trigger)
        return cls(
            id=job.id,
            name=job.name,
            job_trigger_type=job_type,
            job_trigger_config=job_config,
            reports=job.kwargs.get("reports"),
        )

    @staticmethod
    def get_trigger_info_from_scheduler_job(
        trigger: JobTrigger,
    ) -> tuple[str, JobTriggerConfig]:
        match trigger:
            case CustomIntervalTrigger():
                return JobTriggerType.INTERVAL, trigger.trigger_config
            case CustomCronTrigger():
                return JobTriggerType.CRON, trigger.trigger_config
            case CustomDateTrigger():
                return JobTriggerType.DATE, trigger.trigger_config

    @model_validator(mode="before")
    @classmethod
    def clean_data(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["name"] = values.get("name") or None
        return values

    @model_validator(mode="after")
    def validate_job_type(self) -> "Job":
        match self.job_trigger_type:
            case JobTriggerType.INTERVAL:
                if isinstance(self.job_trigger_config, IntervalConfig):
                    return self
            case JobTriggerType.CRON:
                if isinstance(self.job_trigger_config, CronConfig):
                    return self
            case JobTriggerType.DATE:
                if isinstance(self.job_trigger_config, DateConfig):
                    return self
            case _:
                logger.error("Unknonw job type '%s'", self.job_trigger_type)
                raise InvalidJobConfigurationError(f"Unknown job type: {self.job_trigger_type}")
        logger.error(
            "Invalid configuration type '%s' for job type '%s'", type(self.job_trigger_config), self.job_trigger_type
        )
        raise InvalidJobConfigurationError(f"Invalid configuration type for job '{self.job_trigger_type}'")
