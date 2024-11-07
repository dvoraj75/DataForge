from typing import Annotated

from fastapi import APIRouter, Depends

from data_forge.api.dependencies import get_job_service
from data_forge.api.models.base import BasePostResponseModel
from data_forge.api.models.job import JobPostRequest
from data_forge.services.job import JobService

job_router = APIRouter(prefix="/job", tags=["job"])


@job_router.post("")
async def add_job(
    job_data: JobPostRequest, job_service: Annotated[JobService, Depends(get_job_service)]
) -> BasePostResponseModel:
    job_service.add_job(job_data)
    return BasePostResponseModel()
