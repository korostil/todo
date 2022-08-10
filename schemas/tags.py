from pydantic import BaseModel, Field, validator

from schemas.validators import validate_none

__all__ = ('TagResponse', 'CreateTagRequest', 'UpdateTagRequest')


class TagBase(BaseModel):
    title: str | None


class TagResponse(TagBase):
    id: int


class CreateTagRequest(TagBase):
    title: str = Field(min_length=1, max_length=31)


class UpdateTagRequest(TagBase):
    title: str | None = Field(None, min_length=1, max_length=31)

    _validate_title = validator('title', allow_reuse=True)(validate_none)
