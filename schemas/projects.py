from datetime import datetime

from pydantic import BaseModel, Field

__all__ = ('ProjectResponse', 'CreateProjectRequest', 'UpdateProjectRequest')


class ProjectBase(BaseModel):
    archived: bool = False
    description: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)

    class Config:
        orm_mode = True


class ProjectResponse(ProjectBase):
    created_at: datetime
    id: int


class CreateProjectRequest(ProjectBase):
    ...


UpdateProjectRequest = CreateProjectRequest
