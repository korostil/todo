from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field, root_validator, validator

from api.exceptions import BadRequest
from schemas.validators import validate_none
from utils.validators import reusable_validator

__all__ = (
    'GoalResponse',
    'CreateGoalRequest',
    'UpdateGoalRequest',
    'RetrieveGoalListRequest',
)


class GoalBase(BaseModel):
    month: int | None
    title: str | None
    year: int | None


class GoalResponse(GoalBase):
    achieved_at: datetime | None
    created_at: datetime
    id: int
    projects: list[int]

    @root_validator
    def validate_goal(cls, values: dict) -> dict:
        values['is_achieved'] = values.get('achieved_at') is not None
        return values


class CreateGoalRequest(GoalBase):
    month: int | None = Field(None, ge=1, le=12)
    title: str = Field(min_length=1, max_length=255)
    year: int | None = Field(None, ge=2022)


class UpdateGoalRequest(GoalBase):
    title: str | None = Field(None, min_length=1, max_length=255)

    _validate_title = reusable_validator('title')(validate_none)


class RetrieveGoalListRequest(BaseModel):
    achieved: bool | None = Query(None)
    year: int | None = Query(None, ge=datetime.now().year)
    month: int | None = Query(None, ge=1, le=12)
    search: str | None = Query(None)

    @validator('month')
    def validate_month(cls, value: int | None, values: dict) -> int | None:
        if value is not None and values.get('year') is None:
            raise BadRequest('Request should contain both the year and month')
        return value
