from typing import Annotated

from fastapi import Depends, Request

from data_forge.services.job import JobService
from data_forge.services.report import ReportService


def get_report_service() -> ReportService:
    return ReportService()


def get_job_service(
    report_service: Annotated[ReportService, Depends(get_report_service)], request: Request
) -> JobService:
    return JobService(
        app=request.app,
        report_service=report_service,
    )
