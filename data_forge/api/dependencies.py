from fastapi import Request

from data_forge.services.job import JobService


def get_job_service(request: Request) -> JobService:
    return JobService(
        app=request.app,
    )
