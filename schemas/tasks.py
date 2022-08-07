from datetime import datetime

from pydantic import BaseModel, Field

__all__ = ('TaskResponse', 'CreateTaskRequest', 'UpdateTaskRequest')


class TaskBase(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    due: datetime | None
    title: str = Field(min_length=1, max_length=255)


class TaskResponse(TaskBase):
    created_at: datetime
    id: int

    class Config:
        orm_mode = True


class CreateTaskRequest(TaskBase):
    ...


UpdateTaskRequest = CreateTaskRequest
