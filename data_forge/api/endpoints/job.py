from typing import Annotated

from fastapi import APIRouter, Depends

from data_forge.api.dependencies import get_job_service
from data_forge.api.models.base import BaseDeleteNoContentResponseModel, BasePostResponseModel
from data_forge.api.models.job import JobGetListResponse, JobGetResponse, JobPostRequest
from data_forge.services.job import JobService

job_router = APIRouter(prefix="/job", tags=["job"])


@job_router.post("")
async def add_job(
    job_data: JobPostRequest, job_service: Annotated[JobService, Depends(get_job_service)]
) -> BasePostResponseModel:
    job_service.add_job(job_data)
    return BasePostResponseModel()


@job_router.get("")
async def get_all_jobs(job_service: Annotated[JobService, Depends(get_job_service)]) -> JobGetListResponse:
    return JobGetListResponse(jobs=job_service.get_all_jobs())


@job_router.get("/{job_id}")
async def get_job(job_id: str, job_service: Annotated[JobService, Depends(get_job_service)]) -> JobGetResponse:
    return JobGetResponse(job=job_service.get_job(job_id))


@job_router.delete("")
async def remove_all_jobs(
    job_service: Annotated[JobService, Depends(get_job_service)]
) -> BaseDeleteNoContentResponseModel:
    job_service.remove_all_jobs()
    return BaseDeleteNoContentResponseModel()


@job_router.delete("/{job_id}")
async def remove_job(
    job_id: str, job_service: Annotated[JobService, Depends(get_job_service)]
) -> BaseDeleteNoContentResponseModel:
    job_service.remove_job(job_id)
    return BaseDeleteNoContentResponseModel()
