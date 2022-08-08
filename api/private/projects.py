from databases.interfaces import Record
from fastapi import APIRouter, Query, status
from sqlalchemy import delete, insert, select, update

from api.exceptions import NotFound
from app.database import database
from models import Project
from schemas.projects import CreateProjectRequest, ProjectResponse, UpdateProjectRequest

router = APIRouter()


@router.get('/projects/', tags=['projects'], response_model=list[ProjectResponse])
async def read_projects_list(archived: bool | None = Query(None)) -> list[Record]:
    query = select(Project)

    if archived is not None:
        query.filter(Project.archived == archived)

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
    query = insert(Project).values(**request.dict()).returning(Project)
    project = await database.fetch_one(query)
    return project  # type: ignore


@router.put('/projects/{pk}/', tags=['projects'], response_model=ProjectResponse)
async def update_project(pk: int, request: UpdateProjectRequest) -> Record:
    update_data = request.dict(exclude_none=True)

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
