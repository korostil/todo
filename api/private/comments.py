from databases.interfaces import Record
from fastapi import APIRouter, status
from sqlalchemy import delete, insert, select, update

from api.exceptions import NotFound
from app.database import database
from models import Comment
from schemas.comments import CommentResponse, CreateCommentRequest, UpdateCommentRequest

router = APIRouter()


@router.get('/comments/', tags=['tasks'], response_model=list[CommentResponse])
async def read_comments_list() -> list[Record]:
    query = select(Comment)
    comments = await database.fetch_all(query)
    return comments


@router.get('/comments/{pk}/', tags=['tasks'], response_model=CommentResponse)
async def read_comment(pk: int) -> Record:
    query = select(Comment).filter(Comment.id == pk)
    comment = await database.fetch_one(query)
    if comment is None:
        raise NotFound(f'comment with pk={pk} not found')
    return comment


@router.post(
    '/comments/',
    tags=['tasks'],
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(request: CreateCommentRequest) -> Record:
    query = insert(Comment).values(**request.dict()).returning(Comment)
    comment = await database.fetch_one(query)
    return comment  # type: ignore


@router.put('/comments/{pk}/', tags=['tasks'], response_model=CommentResponse)
async def update_comment(pk: int, request: UpdateCommentRequest) -> Record:
    update_data = request.dict(exclude_unset=True)

    if update_data:
        query = (
            update(Comment)
            .where(Comment.id == pk)
            .values(**update_data)
            .returning(Comment)
        )
    else:
        query = select(Comment).where(Comment.id == pk)

    comment = await database.fetch_one(query)
    if comment is None:
        raise NotFound(f'comment with pk={pk} not found')

    return comment


@router.delete(
    '/comments/{pk}/', tags=['tasks'], status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(pk: int) -> None:
    query = delete(Comment).where(Comment.id == pk).returning(Comment.id)
    comment = await database.fetch_val(query)
    if comment is None:
        raise NotFound(f'comment with pk={pk} not found')
