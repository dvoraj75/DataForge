from data_forge.api.models.base import BaseGetResponseModel
from data_forge.core.models import Job


class JobGetResponse(BaseGetResponseModel):
    job: Job


class JobGetListResponse(BaseGetResponseModel):
    jobs: list[Job]


class JobPostRequest(Job):
    pass
