import funcy
from fastapi import APIRouter, status
from sqlalchemy import delete, insert, select, update

from api.exceptions import NotFound
from app.database import database
from models import Goal, Project
from schemas.goals import CreateGoalRequest, GoalResponse, UpdateGoalRequest
from services.exceptions import DoesNotExist
from services.goals import get_one_goal

router = APIRouter()


@router.get('/goals/', tags=['goals'], response_model=list[GoalResponse])
async def read_goals_list() -> list[dict]:
    query = select(Goal)
    goals = await database.fetch_all(query)

    response = []
    for goal in goals:
        response_item = dict(goal)
        response_item['projects'] = funcy.lpluck_attr(
            'id',
            await database.fetch_all(
                select(Project).filter(Project.goal_id == response_item['id'])
            ),
        )
        response.append(response_item)
    return response


@router.get('/goals/{pk}/', tags=['goals'], response_model=GoalResponse)
async def read_goal(pk: int) -> dict:
    with funcy.reraise(DoesNotExist, NotFound(f'goal with pk={pk} not found')):
        goal = await get_one_goal(pk=pk)

    response = dict(goal)  # type: ignore
    response['projects'] = funcy.lpluck_attr(
        'id', await database.fetch_all(select(Project).filter(Project.goal_id == pk))
    )
    return response


@router.post(
    '/goals/',
    tags=['goals'],
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_goal(request: CreateGoalRequest) -> dict:
    query = insert(Goal).values(**request.dict()).returning(Goal)
    goal = await database.fetch_one(query)
    response = dict(goal)  # type: ignore
    response['projects'] = []
    return response


@router.put('/goals/{pk}/', tags=['goals'], response_model=GoalResponse)
async def update_goal(pk: int, request: UpdateGoalRequest) -> dict:
    update_data = request.dict(exclude_unset=True)

    if update_data:
        query = update(Goal).where(Goal.id == pk).values(**update_data).returning(Goal)
    else:
        query = select(Goal).where(Goal.id == pk)

    goal = await database.fetch_one(query)
    if goal is None:
        raise NotFound(f'goal with pk={pk} not found')

    response = dict(goal)
    response['projects'] = funcy.lpluck_attr(
        'id', await database.fetch_all(select(Project).filter(Project.goal_id == pk))
    )
    return response


@router.delete('/goals/{pk}/', tags=['goals'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(pk: int) -> None:
    with funcy.reraise(DoesNotExist, NotFound(f'goal with pk={pk} not found')):
        await get_one_goal(pk=pk)

    await database.execute(delete(Project).where(Project.goal_id == pk))
    await database.execute(delete(Goal).where(Goal.id == pk).returning(Goal.id))
