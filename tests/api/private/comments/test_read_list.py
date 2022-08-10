from fastapi import status

from main import app
from tests.api.helpers import serialize_error_response
from tests.api.private.comments.helpers import serialize_comment_response
from tests.factories import CommentFactory


class TestReadCommentList:
    async def _setup(self):
        self.url = app.url_path_for('read_comments_list')

    async def test_successfully_read_list(self, client):
        await self._setup()
        comments = await CommentFactory.create_batch(size=2)

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_comment_response(comments)

    async def test_empty_list(self, client):
        await self._setup()
        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_comment_response([])

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
