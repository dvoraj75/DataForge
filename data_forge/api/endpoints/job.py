from fastapi import APIRouter, Request

job_router = APIRouter(prefix='/job', tags=['job'])


@job_router.get('')
async def get_jobs(request: Request):
    pass
