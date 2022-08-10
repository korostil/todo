from pydantic import BaseModel, Field

__all__ = ('TagResponse', 'CreateTagRequest', 'UpdateTagRequest')


class TagBase(BaseModel):
    title: str | None


class TagResponse(TagBase):
    id: int


class CreateTagRequest(TagBase):
    title: str = Field(min_length=1, max_length=31)


class UpdateTagRequest(TagBase):
    title: str | None = Field(None, min_length=1, max_length=31)
