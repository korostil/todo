import funcy

from models import Project
from tests.api.helpers import serialize_response


def serialize_project(project: Project) -> dict:
    return {
        'archived': project.archived,
        'created_at': project.created_at.isoformat(),
        'description': project.description,
        'id': project.id,
        'title': project.title,
        'space': project.space,
    }


serialize_project_response = funcy.partial(
    serialize_response, serializer=serialize_project
)
