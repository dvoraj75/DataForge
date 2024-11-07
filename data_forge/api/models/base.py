from fastapi import status
from pydantic import BaseModel, Field


class BaseResponseModel(BaseModel):
    status: str = Field(description="Response message", default="OK")


class BaseGetResponseModel(BaseResponseModel):
    code: int = Field(description="HTTP Response code", default=status.HTTP_200_OK)


class BasePostResponseModel(BaseResponseModel):
    code: int = Field(description="HTTP Response code", default=status.HTTP_201_CREATED)
