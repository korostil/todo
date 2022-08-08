from datetime import datetime

from pydantic import BaseModel, Field

__all__ = ('TaskResponse', 'CreateTaskRequest', 'UpdateTaskRequest')


class TaskBase(BaseModel):
    description: str | None
    due: datetime | None
    title: str | None


class TaskResponse(TaskBase):
    created_at: datetime
    id: int


class CreateTaskRequest(TaskBase):
    description: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)


class UpdateTaskRequest(TaskBase):
    description: str | None = Field(None, min_length=1, max_length=255)
    title: str | None = Field(None, min_length=1, max_length=255)
