from datetime import datetime

from pydantic import BaseModel, Field, validator

from schemas.validators import validate_datetime, validate_space

__all__ = ('TaskResponse', 'CreateTaskRequest', 'UpdateTaskRequest')


class TaskBase(BaseModel):
    description: str | None
    due: datetime | None
    title: str | None
    space: int | None


class TaskResponse(TaskBase):
    created_at: datetime
    id: int


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
    _validate_space = validator('space', allow_reuse=True)(validate_space)
