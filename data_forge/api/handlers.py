from fastapi import Request, status
from fastapi.responses import JSONResponse

from data_forge.core.exceptions import InvalidConfigurationError, JobDoesNotExistError


async def invalid_configration_exception_handler(  # noqa: RUF029
    _: Request, exception: InvalidConfigurationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": 422, "detail": str(exception)},
    )


async def job_does_not_exist_error_handler(_: Request, exception: JobDoesNotExistError) -> JSONResponse:  # noqa: RUF029
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"code": 404, "detail": str(exception)},
    )
