import funcy
from databases.interfaces import Record
from fastapi import APIRouter, status
from sqlalchemy import select

from api.exceptions import NotFound
from app.database import database
from models import Tag
from schemas.tags import CreateTagRequest, TagResponse, UpdateTagRequest
from services.exceptions import DoesNotExist
from services.tags import create_one_tag, delete_one_tag, get_one_tag, update_one_tag

router = APIRouter()


@router.get('/tags/', tags=['tasks'], response_model=list[TagResponse])
async def read_tags_list() -> list[Record]:
    query = select(Tag)
    tags = await database.fetch_all(query)
    return tags


@router.get('/tags/{pk}/', tags=['tasks'], response_model=TagResponse)
async def read_tag(pk: int) -> Record:
    with funcy.reraise(DoesNotExist, NotFound(f'tag with pk={pk} not found')):
        tag: Record = await get_one_tag(pk=pk)
    return tag


@router.post(
    '/tags/',
    tags=['tasks'],
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(request: CreateTagRequest) -> Record:
    tag: Record = await create_one_tag(data=request.dict())
    return tag


@router.put('/tags/{pk}/', tags=['tasks'], response_model=TagResponse)
async def update_tag(pk: int, request: UpdateTagRequest) -> Record:
    update_data = request.dict(exclude_unset=True)

    with funcy.reraise(DoesNotExist, NotFound(f'tag with pk={pk} not found')):
        tag: Record = await update_one_tag(pk=pk, data=update_data)

    return tag


@router.delete('/tags/{pk}/', tags=['tasks'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(pk: int) -> None:
    with funcy.reraise(DoesNotExist, NotFound(f'tag with pk={pk} not found')):
        await delete_one_tag(pk=pk)
