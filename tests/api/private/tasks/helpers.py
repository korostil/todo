import funcy

from models import Task
from tests.api.helpers import serialize_response


def serialize_task(task: Task) -> dict:
    return {
        'created_at': task.created_at.isoformat(),
        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        'description': task.description,
        'due': task.due.isoformat() if task.due else None,
        'id': task.id,
        'is_completed': task.completed_at is not None,
        'title': task.title,
        'space': task.space,
    }


serialize_task_response = funcy.partial(serialize_response, serializer=serialize_task)
