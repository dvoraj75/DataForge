import logging

from apscheduler.jobstores.base import JobLookupError
from fastapi import FastAPI

from data_forge.api.models.job import JobPostRequest
from data_forge.core.enums import JobTriggerType
from data_forge.core.exceptions import JobDoesNotExistError
from data_forge.core.models import Job
from data_forge.core.triggers import CustomCronTrigger, CustomDateTrigger, CustomIntervalTrigger, JobTrigger
from data_forge.services.report import ReportService

logger = logging.getLogger(__name__)


class JobService:
    JOB_TYPE_TRIGGER_MAP: dict[str, JobTrigger] = {
        JobTriggerType.INTERVAL: CustomIntervalTrigger,
        JobTriggerType.DATE: CustomDateTrigger,
        JobTriggerType.CRON: CustomCronTrigger,
    }

    def __init__(self, app: FastAPI, report_service: ReportService) -> None:
        self.app = app
        self.report_service = report_service

    def add_job(self, job: JobPostRequest) -> None:
        logger.info("Adding job with id '%s'.", job.id)
        self.app.state.scheduler.add_job(
            func=self.report_service.create_reports,
            trigger=self.get_trigger_for_job(job),
            name=job.name,
            id=str(job.id),
            kwargs={"reports": job.reports},
        )

    def get_trigger_for_job(self, job: JobPostRequest) -> JobTrigger:
        return self.JOB_TYPE_TRIGGER_MAP.get(job.job_trigger_type)(job.job_trigger_config)

    def get_all_jobs(self) -> list[Job]:
        return [Job.from_scheduler_job(job) for job in self.app.state.scheduler.get_jobs()]

    def get_job(self, job_id: str) -> Job:
        logger.info("Getting job with id '%s'.", job_id)
        if job := self.app.state.scheduler.get_job(job_id):
            return Job.from_scheduler_job(job)
        logger.error("Job with id '%s' not found.", job_id)
        raise JobDoesNotExistError(f"Job with id '{job_id}' not found")

    def remove_all_jobs(self) -> None:
        logger.info("Removing all jobs.")
        self.app.state.scheduler.remove_all_jobs()

    def remove_job(self, job_id: str) -> None:
        logger.info("Removing job with id '%s'.", job_id)
        try:
            self.app.state.scheduler.remove_job(job_id)
        except JobLookupError:
            logger.error("Job with id '%s' not found.", job_id)
            raise JobDoesNotExistError(f"Job with id '{job_id}' not found")
