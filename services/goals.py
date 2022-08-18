from databases.interfaces import Record
from sqlalchemy import select

from app.database import database
from models import Goal
from services.exceptions import DoesNotExist


async def get_one_goal(pk: int | None = None) -> Record | None:
    if pk is None:
        return None

    query = select(Goal).filter(Goal.id == pk)
    goal = await database.fetch_one(query)
    if goal is None:
        raise DoesNotExist

    return goal
