import funcy

from models import Goal
from tests.api.helpers import serialize_response


def serialize_goal(goal: Goal) -> dict:
    return {
        'created_at': goal.created_at.isoformat(),
        'id': goal.id,
        'month': goal.month,
        'title': goal.title,
        'week': goal.week,
        'year': goal.year,
    }


serialize_goal_response = funcy.partial(serialize_response, serializer=serialize_goal)
