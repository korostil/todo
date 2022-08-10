from databases.interfaces import Record
from fastapi import APIRouter, status
from sqlalchemy import delete, insert, select, update

from api.exceptions import NotFound
from app.database import database
from models import Tag
from schemas.tags import CreateTagRequest, TagResponse, UpdateTagRequest

router = APIRouter()


@router.get('/tags/', tags=['tasks'], response_model=list[TagResponse])
async def read_tags_list() -> list[Record]:
    query = select(Tag)
    tags = await database.fetch_all(query)
    return tags


@router.get('/tags/{pk}/', tags=['tasks'], response_model=TagResponse)
async def read_tag(pk: int) -> Record:
    query = select(Tag).filter(Tag.id == pk)
    tag = await database.fetch_one(query)
    if tag is None:
        raise NotFound(f'tag with pk={pk} not found')
    return tag


@router.post(
    '/tags/',
    tags=['tasks'],
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(request: CreateTagRequest) -> Record:
    query = insert(Tag).values(**request.dict()).returning(Tag)
    tag = await database.fetch_one(query)
    return tag  # type: ignore


@router.put('/tags/{pk}/', tags=['tasks'], response_model=TagResponse)
async def update_tag(pk: int, request: UpdateTagRequest) -> Record:
    update_data = request.dict(exclude_unset=True)

    if update_data:
        query = update(Tag).where(Tag.id == pk).values(**update_data).returning(Tag)
    else:
        query = select(Tag).where(Tag.id == pk)

    tag = await database.fetch_one(query)
    if tag is None:
        raise NotFound(f'tag with pk={pk} not found')

    return tag


@router.delete('/tags/{pk}/', tags=['tasks'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(pk: int) -> None:
    query = delete(Tag).where(Tag.id == pk).returning(Tag.id)
    tag = await database.fetch_val(query)
    if tag is None:
        raise NotFound(f'tag with pk={pk} not found')
