from databases.interfaces import Record
from fastapi import APIRouter, status
from sqlalchemy import delete, insert, select, update

from api.exceptions import NotFound
from app.database import database
from models import Goal
from schemas.goals import CreateGoalRequest, GoalResponse, UpdateGoalRequest

router = APIRouter()


@router.get('/goals/', tags=['goals'], response_model=list[GoalResponse])
async def read_goals_list() -> list[Record]:
    query = select(Goal)
    goals = await database.fetch_all(query)
    return goals


@router.get('/goals/{pk}/', tags=['goals'], response_model=GoalResponse)
async def read_goal(pk: int) -> Record:
    query = select(Goal).filter(Goal.id == pk)
    goal = await database.fetch_one(query)
    if goal is None:
        raise NotFound(f'goal with pk={pk} not found')
    return goal


@router.post(
    '/goals/',
    tags=['goals'],
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_goal(request: CreateGoalRequest) -> Record:
    query = insert(Goal).values(**request.dict()).returning(Goal)
    goal = await database.fetch_one(query)
    return goal  # type: ignore


@router.put('/goals/{pk}/', tags=['goals'], response_model=GoalResponse)
async def update_goal(pk: int, request: UpdateGoalRequest) -> Record:
    update_data = request.dict(exclude_unset=True)

    if update_data:
        query = update(Goal).where(Goal.id == pk).values(**update_data).returning(Goal)
    else:
        query = select(Goal).where(Goal.id == pk)

    goal = await database.fetch_one(query)
    if goal is None:
        raise NotFound(f'goal with pk={pk} not found')

    return goal


@router.delete('/goals/{pk}/', tags=['goals'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(pk: int) -> None:
    query = delete(Goal).where(Goal.id == pk).returning(Goal.id)
    goal = await database.fetch_val(query)
    if goal is None:
        raise NotFound(f'goal with pk={pk} not found')
