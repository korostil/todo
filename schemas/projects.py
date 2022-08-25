from datetime import datetime

from pydantic import BaseModel, Field, root_validator, validator

from schemas.validators import HEX_COLOR_REGEX, validate_none, validate_space

__all__ = ('ProjectResponse', 'CreateProjectRequest', 'UpdateProjectRequest')


class ProjectBase(BaseModel):
    color: str | None
    description: str | None
    goal_id: int | None
    title: str | None
    space: int | None


class ProjectResponse(ProjectBase):
    archived_at: datetime | None
    created_at: datetime
    id: int
    tasks: list[int]

    @root_validator
    def validate_project(cls, values: dict) -> dict:
        values['is_archived'] = values.get('archived_at') is not None
        return values


class CreateProjectRequest(ProjectBase):
    color: str | None = Field(None, regex=HEX_COLOR_REGEX)
    description: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    space: int

    _validate_space = validator('space', allow_reuse=True)(validate_space)


class UpdateProjectRequest(ProjectBase):
    color: str | None = Field(None, regex=HEX_COLOR_REGEX)
    description: str | None = Field(None, min_length=1, max_length=255)
    title: str | None = Field(None, min_length=1, max_length=255)

    _validate_description = validator('description', allow_reuse=True)(validate_none)
    _validate_title = validator('title', allow_reuse=True)(validate_none)
    _validate_space = validator('space', allow_reuse=True)(validate_space)
