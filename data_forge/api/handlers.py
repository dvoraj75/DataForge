from fastapi import Request, status
from fastapi.responses import JSONResponse

from data_forge.core.exceptions import InvalidJobConfigurationError


async def invalid_job_configration_exception_handler(  # noqa: RUF029
    _: Request, exception: InvalidJobConfigurationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": 422, "detail": str(exception)},
    )
