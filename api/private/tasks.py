from databases.interfaces import Record
from fastapi import APIRouter, status
from sqlalchemy import delete, insert, select, update

from api.exceptions import NotFound
from app.database import database
from models import Task
from schemas.tasks import CreateTaskRequest, TaskResponse, UpdateTaskRequest

router = APIRouter()


@router.get('/tasks/', tags=['tasks'], response_model=list[TaskResponse])
async def read_tasks_list() -> list[Record]:
    query = select(Task)
    tasks = await database.fetch_all(query)
    return tasks


@router.get('/tasks/{pk}/', tags=['tasks'], response_model=TaskResponse)
async def read_task(pk: int) -> Record:
    query = select(Task).filter(Task.id == pk)
    task = await database.fetch_one(query)
    if task is None:
        raise NotFound(f'task with pk={pk} not found')
    return task


@router.post(
    '/tasks/',
    tags=['tasks'],
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(request: CreateTaskRequest) -> Record:
    query = insert(Task).values(**request.dict()).returning(Task)
    task = await database.fetch_one(query)
    return task  # type: ignore


@router.put('/tasks/{pk}/', tags=['tasks'], response_model=TaskResponse)
async def update_task(pk: int, request: UpdateTaskRequest) -> Record:
    update_data = request.dict(exclude_unset=True)

    if update_data:
        query = update(Task).where(Task.id == pk).values(**update_data).returning(Task)
    else:
        query = select(Task).where(Task.id == pk)

    task = await database.fetch_one(query)
    if task is None:
        raise NotFound(f'task with pk={pk} not found')

    return task


@router.delete('/tasks/{pk}/', tags=['tasks'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(pk: int) -> None:
    query = delete(Task).where(Task.id == pk).returning(Task.id)
    task = await database.fetch_val(query)
    if task is None:
        raise NotFound(f'task with pk={pk} not found')
