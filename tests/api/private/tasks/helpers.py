import funcy

from models import Task
from tests.api.helpers import serialize_response


def serialize_task(task: Task) -> dict:
    return {
        'created_at': task.created_at.isoformat(),
        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        'decisive': task.decisive,
        'description': task.description,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'due_time': task.due_time.isoformat() if task.due_time else None,
        'id': task.id,
        'is_completed': task.completed_at is not None,
        'project_id': task.project_id,
        'space': task.space,
        'title': task.title,
    }


serialize_task_response = funcy.partial(serialize_response, serializer=serialize_task)
