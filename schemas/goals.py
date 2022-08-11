from datetime import datetime

from pydantic import BaseModel, Field, validator

from schemas.validators import validate_none

__all__ = ('GoalResponse', 'CreateGoalRequest', 'UpdateGoalRequest')


class GoalBase(BaseModel):
    month: int | None
    title: str | None
    week: int | None
    year: int | None


class GoalResponse(GoalBase):
    created_at: datetime
    id: int


class CreateGoalRequest(GoalBase):
    month: int | None = Field(None, ge=1, le=12)
    title: str = Field(min_length=1, max_length=255)
    week: int | None = Field(None, ge=1, le=52)
    year: int | None = Field(None, ge=2022)


class UpdateGoalRequest(GoalBase):
    title: str | None = Field(None, min_length=1, max_length=255)

    _validate_title = validator('title', allow_reuse=True)(validate_none)
