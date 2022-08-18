import funcy

from models import Project
from tests.api.helpers import serialize_response


def serialize_project(project: Project) -> dict:
    return {
        'archived_at': project.archived_at.isoformat() if project.archived_at else None,
        'color': project.color,
        'created_at': project.created_at.isoformat() if project.created_at else None,
        'description': project.description,
        'goal_id': project.goal_id,
        'id': project.id,
        'is_archived': project.archived_at is not None,
        'title': project.title,
        'space': project.space,
    }


serialize_project_response = funcy.partial(
    serialize_response, serializer=serialize_project
)
