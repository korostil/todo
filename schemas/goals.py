from datetime import datetime

from pydantic import BaseModel, Field, validator

from schemas.validators import validate_none, validate_status

__all__ = ('GoalResponse', 'CreateGoalRequest', 'UpdateGoalRequest')


class GoalBase(BaseModel):
    month: int | None
    status: int
    title: str | None
    week: int | None
    year: int | None


class GoalResponse(GoalBase):
    created_at: datetime
    id: int
    projects: list[int]


class CreateGoalRequest(GoalBase):
    month: int | None = Field(None, ge=1, le=12)
    title: str = Field(min_length=1, max_length=255)
    week: int | None = Field(None, ge=1, le=52)
    year: int | None = Field(None, ge=2022)

    _validate_status = validator('status', allow_reuse=True)(validate_status)


class UpdateGoalRequest(GoalBase):
    status: int | None  # type: ignore
    title: str | None = Field(None, min_length=1, max_length=255)

    _validate_status = validator('status', allow_reuse=True)(validate_status)
    _validate_title = validator('title', allow_reuse=True)(validate_none)
