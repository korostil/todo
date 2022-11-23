from datetime import datetime

from pydantic import BaseModel, Field

from schemas.validators import validate_none
from utils.validators import reusable_validator

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

    _validate_text = reusable_validator('text')(validate_none)
