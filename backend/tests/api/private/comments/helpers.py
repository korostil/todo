import funcy

from models import Comment
from tests.api.helpers import serialize_response


def serialize_comment(comment: Comment) -> dict:
    return {
        'created_at': comment.created_at.isoformat(),
        'id': comment.id,
        'text': comment.text,
    }


serialize_comment_response = funcy.partial(
    serialize_response, serializer=serialize_comment
)
