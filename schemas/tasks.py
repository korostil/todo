from datetime import date, datetime, time

from fastapi import Query
from pydantic import BaseModel, Field, root_validator

from app.settings import settings
from schemas.validators import (
    validate_date,
    validate_none,
    validate_space,
    validate_time,
)
from utils.validators import reusable_validator

__all__ = (
    'TaskResponse',
    'CreateTaskRequest',
    'UpdateTaskRequest',
    'RetrieveTasksListRequest',
)


class TaskBase(BaseModel):
    decisive: bool | None
    description: str | None
    due_date: date | None
    due_time: time | None
    project_id: int | None
    space: int | None
    title: str | None


class TaskResponse(TaskBase):
    created_at: datetime
    completed_at: datetime | None
    decisive: bool
    id: int

    @root_validator
    def validate_task(cls, values: dict) -> dict:
        values['is_completed'] = values.get('completed_at') is not None
        return values


class CreateTaskRequest(TaskBase):
    decisive: bool = False
    description: str | None = Field(None, min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    space: int

    _validate_due_date = reusable_validator('due_date', pre=True)(validate_date)
    _validate_due_time = reusable_validator('due_time', pre=True)(validate_time)
    _validate_space = reusable_validator('space')(validate_space)


class UpdateTaskRequest(TaskBase):
    description: str | None = Field(None, min_length=1, max_length=255)
    title: str | None = Field(None, min_length=1, max_length=255)

    _validate_decisive = reusable_validator('decisive')(validate_none)
    _validate_due_date = reusable_validator('due_date', pre=True)(validate_date)
    _validate_due_time = reusable_validator('due_time', pre=True)(validate_time)
    _validate_title = reusable_validator('title')(validate_none)
    _validate_space = reusable_validator('space')(validate_space)


class RetrieveTasksListRequest(BaseModel):
    decisive: bool | None = Query(None)
    due_from: date | None = Query(None)
    due_to: date | None = Query(None)
    completed: bool | None = Query(None)
    limit: int | None = Query(
        settings.max_tasks_per_page, gt=0, le=settings.max_tasks_per_page
    )
    offset: int | None = Query(0, ge=0)
    project_id: int | None = Query(None)
    search: str | None = Query(None)
