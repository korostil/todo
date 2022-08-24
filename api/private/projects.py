import funcy
from databases.interfaces import Record
from fastapi import APIRouter, Query, status
from sqlalchemy import func, select

from api.exceptions import NotFound
from app.database import database
from models import Project
from schemas.projects import CreateProjectRequest, ProjectResponse, UpdateProjectRequest
from services.exceptions import DoesNotExist
from services.goals import get_one_goal
from services.projects import (
    create_one_project,
    delete_one_project,
    get_one_project,
    update_one_project,
)

router = APIRouter()


@router.get('/projects/', tags=['projects'], response_model=list[ProjectResponse])
async def read_projects_list(archived: bool | None = Query(None)) -> list[Record]:
    query = select(Project)

    if archived is not None:
        query = query.filter(
            Project.archived_at.isnot(None)
            if archived
            else Project.archived_at.is_(None)
        )

    projects = await database.fetch_all(query)
    return projects


@router.get('/projects/{pk}/', tags=['projects'], response_model=ProjectResponse)
async def read_project(pk: int) -> Record:
    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        project: Record = await get_one_project(pk=pk)
    return project


@router.post(
    '/projects/',
    tags=['projects'],
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(request: CreateProjectRequest) -> Record:
    with funcy.reraise(
        DoesNotExist, NotFound(f'goal with pk={request.goal_id} not found')
    ):
        await get_one_goal(pk=request.goal_id)

    project: Record = await create_one_project(data=request.dict())
    return project


@router.put('/projects/{pk}/', tags=['projects'], response_model=ProjectResponse)
async def update_project(pk: int, request: UpdateProjectRequest) -> Record:
    update_data = request.dict(exclude_unset=True)
    goal_id = update_data.get('goal_id')

    with funcy.reraise(DoesNotExist, NotFound(f'goal with pk={goal_id} not found')):
        await get_one_goal(pk=goal_id)

    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        project: Record = await update_one_project(pk=pk, data=update_data)

    return project


@router.delete(
    '/projects/{pk}/', tags=['projects'], status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(pk: int) -> None:
    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        await delete_one_project(pk=pk)


@router.post(
    '/projects/{pk}/archive/',
    tags=['projects'],
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
async def archive_project(pk: int) -> Record:
    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        project: Record = await update_one_project(
            pk=pk, data={'archived_at': func.now()}
        )
    return project


@router.post(
    '/projects/{pk}/restore/',
    tags=['projects'],
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
async def restore_project(pk: int) -> Record:
    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        project: Record = await update_one_project(pk=pk, data={'archived_at': None})
    return project
