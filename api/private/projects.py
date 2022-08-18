import funcy
from databases.interfaces import Record
from fastapi import APIRouter, Query, status
from sqlalchemy import delete, func, insert, select, update

from api.exceptions import NotFound
from app.database import database
from models import Project
from schemas.projects import CreateProjectRequest, ProjectResponse, UpdateProjectRequest
from services.exceptions import DoesNotExist
from services.goals import get_one_goal

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
    query = select(Project).filter(Project.id == pk)
    project = await database.fetch_one(query)
    if project is None:
        raise NotFound(f'project with pk={pk} not found')
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

    query = insert(Project).values(**request.dict()).returning(Project)
    project = await database.fetch_one(query)
    return project  # type: ignore


@router.put('/projects/{pk}/', tags=['projects'], response_model=ProjectResponse)
async def update_project(pk: int, request: UpdateProjectRequest) -> Record:
    update_data = request.dict(exclude_unset=True)
    goal_id = update_data.get('goal_id')

    with funcy.reraise(DoesNotExist, NotFound(f'goal with pk={goal_id} not found')):
        await get_one_goal(pk=goal_id)

    if update_data:
        query = (
            update(Project)
            .where(Project.id == pk)
            .values(**update_data)
            .returning(Project)
        )
    else:
        query = select(Project).where(Project.id == pk)

    project = await database.fetch_one(query)
    if project is None:
        raise NotFound(f'project with pk={pk} not found')

    return project


@router.delete(
    '/projects/{pk}/', tags=['projects'], status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(pk: int) -> None:
    query = delete(Project).where(Project.id == pk).returning(Project.id)
    project = await database.fetch_val(query)
    if project is None:
        raise NotFound(f'project with pk={pk} not found')


@router.post(
    '/projects/{pk}/archive/',
    tags=['projects'],
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
async def archive_project(pk: int) -> Record:
    query = (
        update(Project)
        .where(Project.id == pk)
        .values(archived_at=func.now())
        .returning(Project)
    )

    project = await database.fetch_one(query)
    if project is None:
        raise NotFound(f'project with pk={pk} not found')

    return project


@router.post(
    '/projects/{pk}/restore/',
    tags=['projects'],
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
async def restore_project(pk: int) -> Record:
    query = (
        update(Project)
        .where(Project.id == pk)
        .values(archived_at=None)
        .returning(Project)
    )

    project = await database.fetch_one(query)
    if project is None:
        raise NotFound(f'project with pk={pk} not found')

    return project
