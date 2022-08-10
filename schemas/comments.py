from datetime import datetime

from pydantic import BaseModel, Field, validator

__all__ = ('CommentResponse', 'CreateCommentRequest', 'UpdateCommentRequest')


class CommentBase(BaseModel):
    text: str | None


class CommentResponse(CommentBase):
    created_at: datetime
    id: int


class CreateCommentRequest(CommentBase):
    text: str = Field(min_length=1, max_length=1023)


class UpdateCommentRequest(CommentBase):
    text: str | None = Field(None, min_length=1, max_length=1023)

    @validator('text')
    def validate_text(cls, value: str) -> str:
        if not value:
            raise ValueError('none is not an allowed value')
        return value
