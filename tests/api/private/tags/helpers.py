import funcy

from models import Tag
from tests.api.helpers import serialize_response


def serialize_tag(tag: Tag) -> dict:
    return {'id': tag.id, 'title': tag.title}


serialize_tag_response = funcy.partial(serialize_response, serializer=serialize_tag)
