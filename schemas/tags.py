from pydantic import BaseModel, Field, validator

from schemas.validators import HEX_COLOR_REGEX, validate_none

__all__ = ('TagResponse', 'CreateTagRequest', 'UpdateTagRequest')


class TagBase(BaseModel):
    color: str | None
    title: str | None


class TagResponse(TagBase):
    id: int


class CreateTagRequest(TagBase):
    color: str | None = Field(None, regex=HEX_COLOR_REGEX)
    title: str = Field(min_length=1, max_length=31)


class UpdateTagRequest(TagBase):
    color: str | None = Field(None, regex=HEX_COLOR_REGEX)
    title: str | None = Field(None, min_length=1, max_length=31)

    _validate_title = validator('title', allow_reuse=True)(validate_none)
