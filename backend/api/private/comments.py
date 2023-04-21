import funcy
from databases.interfaces import Record
from fastapi import APIRouter, status
from sqlalchemy import select

from api.exceptions import NotFound
from app.database import database
from models import Comment
from schemas.comments import CommentResponse, CreateCommentRequest, UpdateCommentRequest
from services.comments import (
    create_one_comment,
    delete_one_comment,
    get_one_comment,
    update_one_comment,
)
from services.exceptions import DoesNotExist

router = APIRouter()


@router.get('/comments/', tags=['tasks'], response_model=list[CommentResponse])
async def read_comments_list() -> list[Record]:
    query = select(Comment)
    comments = await database.fetch_all(query)
    return comments


@router.get('/comments/{pk}/', tags=['tasks'], response_model=CommentResponse)
async def read_comment(pk: int) -> Record:
    with funcy.reraise(DoesNotExist, NotFound(f'comment with pk={pk} not found')):
        comment: Record = await get_one_comment(pk=pk)
    return comment


@router.post(
    '/comments/',
    tags=['tasks'],
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(request: CreateCommentRequest) -> Record:
    comment: Record = await create_one_comment(data=request.dict())
    return comment


@router.put('/comments/{pk}/', tags=['tasks'], response_model=CommentResponse)
async def update_comment(pk: int, request: UpdateCommentRequest) -> Record:
    update_data = request.dict(exclude_unset=True)

    with funcy.reraise(DoesNotExist, NotFound(f'comment with pk={pk} not found')):
        comment: Record = await update_one_comment(pk=pk, data=update_data)

    return comment


@router.delete(
    '/comments/{pk}/', tags=['tasks'], status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(pk: int) -> None:
    with funcy.reraise(DoesNotExist, NotFound(f'comment with pk={pk} not found')):
        await delete_one_comment(pk=pk)
