import funcy
from databases.interfaces import Record
from fastapi import APIRouter, Query, status
from sqlalchemy import delete, func, select

from api.exceptions import NotFound
from app.database import database
from models import Project, Task
from schemas.projects import CreateProjectRequest, ProjectResponse, UpdateProjectRequest
from services.exceptions import DoesNotExist
from services.goals import get_one_goal
from services.projects import create_one_project, get_one_project, update_one_project
from services.spaces import Space

router = APIRouter()


@router.get('/projects/', tags=['projects'], response_model=list[ProjectResponse])
async def read_projects_list(
    archived: bool | None = Query(None),
    space: Space | None = Query(None),
    search: str | None = Query(None),
) -> list[dict]:
    query = select(Project)

    if archived is not None:
        query = query.filter(
            Project.archived_at.isnot(None)
            if archived
            else Project.archived_at.is_(None)
        )

    if space is not None:
        query = query.filter(Project.space == space.value)

    if search:
        clause = f'%{search}%'
        query = query.filter(
            Project.title.ilike(clause) | Project.description.ilike(clause)
        )

    projects = await database.fetch_all(query)

    response = []
    for project in projects:
        response_item = dict(project)
        response_item['tasks'] = funcy.lpluck_attr(
            'id',
            await database.fetch_all(
                select(Task).filter(Task.project_id == response_item['id'])
            ),
        )
        response.append(response_item)
    return response


@router.get('/projects/{pk}/', tags=['projects'], response_model=ProjectResponse)
async def read_project(pk: int) -> dict:
    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        project = await get_one_project(pk=pk)

    response = dict(project)
    response['tasks'] = funcy.lpluck_attr(
        'id', await database.fetch_all(select(Task).filter(Task.project_id == pk))
    )
    return response


@router.post(
    '/projects/',
    tags=['projects'],
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(request: CreateProjectRequest) -> dict:
    with funcy.reraise(
        DoesNotExist, NotFound(f'goal with pk={request.goal_id} not found')
    ):
        await get_one_goal(pk=request.goal_id)

    project = await create_one_project(data=request.dict())
    response = dict(project)
    response['tasks'] = []
    return response


@router.put('/projects/{pk}/', tags=['projects'], response_model=ProjectResponse)
async def update_project(pk: int, request: UpdateProjectRequest) -> dict:
    update_data = request.dict(exclude_unset=True)
    goal_id = update_data.get('goal_id')

    with funcy.reraise(DoesNotExist, NotFound(f'goal with pk={goal_id} not found')):
        await get_one_goal(pk=goal_id)

    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        project = await update_one_project(pk=pk, data=update_data)

    response = dict(project)
    response['tasks'] = funcy.lpluck_attr(
        'id', await database.fetch_all(select(Task).filter(Task.project_id == pk))
    )
    return response


@router.delete(
    '/projects/{pk}/', tags=['projects'], status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(pk: int) -> None:
    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        await get_one_project(pk=pk)

    await database.execute(delete(Task).where(Task.project_id == pk))
    await database.execute(
        delete(Project).where(Project.id == pk).returning(Project.id)
    )


@router.post(
    '/projects/{pk}/archive/',
    tags=['projects'],
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
async def archive_project(pk: int) -> dict:
    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        project: Record = await update_one_project(
            pk=pk, data={'archived_at': func.now()}
        )
    response = dict(project)
    response['tasks'] = []
    return response


@router.post(
    '/projects/{pk}/restore/',
    tags=['projects'],
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
async def restore_project(pk: int) -> dict:
    with funcy.reraise(DoesNotExist, NotFound(f'project with pk={pk} not found')):
        project: Record = await update_one_project(pk=pk, data={'archived_at': None})
    response = dict(project)
    response['tasks'] = []
    return response
