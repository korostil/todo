from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field, root_validator, validator

from api.exceptions import BadRequest
from schemas.validators import validate_none, validate_status
from utils.validators import reusable_validator

__all__ = (
    'GoalResponse',
    'CreateGoalRequest',
    'UpdateGoalRequest',
    'RetrieveGoalListRequest',
)


class GoalBase(BaseModel):
    month: int | None
    status: int
    title: str | None
    year: int | None


class GoalResponse(GoalBase):
    archived_at: datetime | None
    created_at: datetime
    id: int
    projects: list[int]

    @root_validator
    def validate_goal(cls, values: dict) -> dict:
        values['is_archived'] = values.get('archived_at') is not None
        return values


class CreateGoalRequest(GoalBase):
    month: int | None = Field(None, ge=1, le=12)
    status: int | None  # type: ignore
    title: str = Field(min_length=1, max_length=255)
    year: int | None = Field(None, ge=2022)

    _validate_status = reusable_validator('status')(validate_status)


class UpdateGoalRequest(GoalBase):
    status: int | None  # type: ignore
    title: str | None = Field(None, min_length=1, max_length=255)

    _validate_status_none = reusable_validator('status')(validate_none)
    _validate_status_value = reusable_validator('status')(validate_status)
    _validate_title = reusable_validator('title')(validate_none)


class RetrieveGoalListRequest(BaseModel):
    archived: bool | None = Query(None)
    year: int | None = Query(None, ge=datetime.now().year)
    month: int | None = Query(None, ge=1, le=12)
    search: str | None = Query(None)

    @validator('month')
    def validate_month(cls, value: int | None, values: dict) -> int | None:
        if value is not None and values.get('year') is None:
            raise BadRequest('Request should contain both the year and month')
        return value
