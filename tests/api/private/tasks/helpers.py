import funcy

from models import Task
from tests.api.helpers import serialize_response


def serialize_task(task: Task) -> dict:
    return {
        'created_at': task.created_at.isoformat(),
        'description': task.description,
        'due': task.due.isoformat() if task.due else None,
        'id': task.id,
        'title': task.title,
        'space': task.space,
    }


serialize_task_response = funcy.partial(serialize_response, serializer=serialize_task)
