import funcy

from models import Goal
from tests.api.helpers import serialize_response


def serialize_goal(goal: Goal) -> dict:
    return {
        'achieved_at': goal.achieved_at.isoformat() if goal.achieved_at else None,
        'created_at': goal.created_at.isoformat(),
        'id': goal.id,
        'is_achieved': goal.achieved_at is not None,
        'month': goal.month,
        'projects': goal.projects or [],
        'title': goal.title,
        'year': goal.year,
    }


serialize_goal_response = funcy.partial(serialize_response, serializer=serialize_goal)
