import funcy

from models import Goal
from tests.api.helpers import serialize_response


def serialize_goal(goal: Goal) -> dict:
    return {
        'archived_at': goal.archived_at.isoformat() if goal.archived_at else None,
        'created_at': goal.created_at.isoformat(),
        'id': goal.id,
        'is_archived': goal.archived_at is not None,
        'month': goal.month,
        'projects': goal.projects or [],
        'status': goal.status,
        'title': goal.title,
        'year': goal.year,
    }


serialize_goal_response = funcy.partial(serialize_response, serializer=serialize_goal)
