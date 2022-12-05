import funcy
from databases.interfaces import Record
from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select

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
    query = select(Task)

    if request.completed is not None:
        query = query.filter(
            Task.completed_at.isnot(None)
            if request.completed
            else Task.completed_at.is_(None)
        )

    if request.search:
        clause = f'%{request.search}%'
        query = query.filter(Task.title.ilike(clause) | Task.description.ilike(clause))

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
