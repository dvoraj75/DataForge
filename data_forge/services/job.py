import logging

from fastapi import FastAPI

from data_forge.api.models.job import JobPostRequest
from data_forge.services.report import ReportService

logger = logging.getLogger(__name__)


class JobService:
    def __init__(self, app: FastAPI, report_service: ReportService) -> None:
        self.app = app
        self.report_service = report_service

    def add_job(self, job: JobPostRequest) -> None:
        self.app.state.scheduler.add_job(
            self.report_service.create_reports,
            job.job_type,
            args=job.reports,
            **job.job_config.model_dump(exclude_unset=True)
        )
