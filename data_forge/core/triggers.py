from typing import TypeAlias, Union

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from data_forge.core import models

JobTrigger: TypeAlias = Union[
    "CustomIntervalTrigger",
    "CustomCronTrigger",
    "CustomDateTrigger",
]


class CustomTriggerMixin:
    def __init__(self, trigger_config: "models.JobTriggerConfig") -> None:
        self.trigger_config = trigger_config
        super().__init__(**self.trigger_config.model_dump(exclude_unset=True))


class CustomIntervalTrigger(CustomTriggerMixin, IntervalTrigger):
    pass


class CustomCronTrigger(CustomTriggerMixin, CronTrigger):
    pass


class CustomDateTrigger(CustomTriggerMixin, DateTrigger):
    pass
