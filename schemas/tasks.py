from datetime import datetime

from pydantic import BaseModel, Field, root_validator, validator

from schemas.validators import validate_datetime, validate_none, validate_space

__all__ = ('TaskResponse', 'CreateTaskRequest', 'UpdateTaskRequest')


class TaskBase(BaseModel):
    description: str | None
    due: datetime | None
    title: str | None
    space: int | None


class TaskResponse(TaskBase):
    created_at: datetime
    completed_at: datetime | None
    id: int

    @root_validator
    def validate_task(cls, values: dict) -> dict:
        values['is_completed'] = values.get('completed_at') is not None
        return values


class CreateTaskRequest(TaskBase):
    description: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    space: int

    _validate_due = validator('due', pre=True, allow_reuse=True)(validate_datetime)
    _validate_space = validator('space', allow_reuse=True)(validate_space)


class UpdateTaskRequest(TaskBase):
    description: str | None = Field(None, min_length=1, max_length=255)
    title: str | None = Field(None, min_length=1, max_length=255)

    _validate_due = validator('due', pre=True, allow_reuse=True)(validate_datetime)
    _validate_description = validator('description', allow_reuse=True)(validate_none)
    _validate_title = validator('title', allow_reuse=True)(validate_none)
    _validate_space = validator('space', allow_reuse=True)(validate_space)
