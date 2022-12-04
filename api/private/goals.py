import funcy
from fastapi import APIRouter, status
from sqlalchemy import delete, select

from api.exceptions import NotFound
from app.database import database
from models import Goal, Project
from schemas.goals import CreateGoalRequest, GoalResponse, UpdateGoalRequest
from services.exceptions import DoesNotExist
from services.goals import create_one_goal, get_one_goal, update_one_goal

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

    response = dict(goal)
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
    goal = await create_one_goal(data=funcy.compact(request.dict()))
    response = dict(goal)
    response['projects'] = []
    return response


@router.put('/goals/{pk}/', tags=['goals'], response_model=GoalResponse)
async def update_goal(pk: int, request: UpdateGoalRequest) -> dict:
    update_data = request.dict(exclude_unset=True)

    with funcy.reraise(DoesNotExist, NotFound(f'goal with pk={pk} not found')):
        goal = await update_one_goal(pk=pk, data=update_data)

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
