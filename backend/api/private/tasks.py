from datetime import date

import funcy
from databases.interfaces import Record
from fastapi import APIRouter, Depends, status
from sqlalchemy import Date, cast, func, nullsfirst, select

from api.exceptions import NotFound
from app.database import database
from models import Task
from schemas.tasks import (
    CreateTaskRequest,
    RetrieveTasksListRequest,
    TaskResponse,
    UpdateTaskRequest,
)
from services.exceptions import DoesNotExist
from services.projects import get_one_project
from services.tasks import (
    create_one_task,
    delete_one_task,
    get_one_task,
    update_one_task,
)

router = APIRouter()


@router.get('/tasks/', tags=['tasks'], response_model=list[TaskResponse])
async def read_tasks_list(
    request: RetrieveTasksListRequest = Depends(),
) -> list[Record]:
    query = select(Task).order_by(
        nullsfirst(Task.completed_at.desc()), Task.created_at.desc(), Task.id.desc()
    )

    if request.completed is not None:
        query = query.filter(
            Task.completed_at.isnot(None)
            if request.completed
            else Task.completed_at.is_(None)
        )

    if request.search:
        clause = f'%{request.search}%'
        query = query.filter(Task.title.ilike(clause) | Task.description.ilike(clause))

    if request.space is not None:
        query = query.filter(Task.space == request.space)

    if request.project_id is not None or request.inbox:
        query = query.filter(Task.project_id == request.project_id)

    if request.decisive is not None:
        query = query.filter(Task.decisive == request.decisive)

    if request.due_from:
        query = query.filter(cast(Task.due_date, Date) >= request.due_from)

    if request.due_to:
        query = query.filter(cast(Task.due_date, Date) <= request.due_to)

    if request.limit:
        query = query.limit(request.limit)

    if request.offset:
        query = query.offset(request.offset)

    tasks = await database.fetch_all(query)

    return tasks


@router.get(
    '/tasks/today/',
    tags=['tasks'],
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
)
async def today_tasks() -> list[Record]:
    query = select(Task).filter(
        (func.DATE(Task.created_at) == date.today())
        | (func.DATE(Task.completed_at) == date.today())
    )

    tasks = await database.fetch_all(query)

    return tasks


@router.get('/tasks/{pk}/', tags=['tasks'], response_model=TaskResponse)
async def read_task(pk: int) -> Record:
    with funcy.reraise(DoesNotExist, NotFound(f'task with pk={pk} not found')):
        task: Record = await get_one_task(pk=pk)
    return task


@router.post(
    '/tasks/',
    tags=['tasks'],
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(request: CreateTaskRequest) -> Record:
    with funcy.reraise(
        DoesNotExist, NotFound(f'project with pk={request.project_id} not found')
    ):
        await get_one_project(pk=request.project_id)
    task: Record = await create_one_task(data=request.dict())
    return task


@router.put('/tasks/{pk}/', tags=['tasks'], response_model=TaskResponse)
async def update_task(pk: int, request: UpdateTaskRequest) -> Record:
    update_data = request.dict(exclude_unset=True)
    project_id = request.project_id

    with funcy.reraise(
        DoesNotExist, NotFound(f'project with pk={project_id} not found')
    ):
        await get_one_project(pk=project_id)

    with funcy.reraise(DoesNotExist, NotFound(f'task with pk={pk} not found')):
        task: Record = await update_one_task(pk=pk, data=update_data)

    return task


@router.delete('/tasks/{pk}/', tags=['tasks'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(pk: int) -> None:
    with funcy.reraise(DoesNotExist, NotFound(f'task with pk={pk} not found')):
        await delete_one_task(pk=pk)


@router.post(
    '/tasks/{pk}/complete/',
    tags=['tasks'],
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
async def complete_task(pk: int) -> Record:
    with funcy.reraise(DoesNotExist, NotFound(f'task with pk={pk} not found')):
        task: Record = await update_one_task(pk=pk, data={'completed_at': func.now()})
    return task


@router.post(
    '/tasks/{pk}/reopen/',
    tags=['tasks'],
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
async def reopen_task(pk: int) -> Record:
    with funcy.reraise(DoesNotExist, NotFound(f'task with pk={pk} not found')):
        task: Record = await update_one_task(pk=pk, data={'completed_at': None})
    return task
