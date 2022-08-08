from datetime import datetime

from pydantic import BaseModel, Field

__all__ = ('ProjectResponse', 'CreateProjectRequest', 'UpdateProjectRequest')


class ProjectBase(BaseModel):
    archived: bool | None
    description: str | None
    title: str | None


class ProjectResponse(ProjectBase):
    created_at: datetime
    id: int


class CreateProjectRequest(ProjectBase):
    archived: bool = False
    description: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)


class UpdateProjectRequest(ProjectBase):
    description: str | None = Field(None, min_length=1, max_length=255)
    title: str | None = Field(None, min_length=1, max_length=255)
