from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Comment
from tests.api.helpers import serialize_error_response
from tests.api.private.comments.helpers import serialize_comment_response
from tests.factories import CommentDataFactory, CommentFactory


class TestUpdateComment:
    async def _setup(self):
        self.comment = await CommentFactory.create()
        self.url = app.url_path_for('update_comment', pk=self.comment.id)

    async def test_successfully_updated(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create()

        response = await client.put(self.url, json=comment_data)

        assert response.status_code == status.HTTP_200_OK
        query = select(Comment).where(Comment.id == self.comment.id)
        comment = await database.fetch_one(query)
        assert comment is not None
        assert response.json() == serialize_comment_response(comment)

    async def test_partially_updated(self, client):
        await self._setup()
        expected_text = 'updated-text'
        comment_data = {'text': expected_text}

        response = await client.put(self.url, json=comment_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['text'] == expected_text

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('update_comment', pk=pk)

        response = await client.put(url, json={})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'comment with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()
        comment_data = CommentDataFactory.create()

        response = await anonymous_client.put(self.url, json=comment_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_text(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create(text='*' * 1024)

        response = await client.put(self.url, json=comment_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'text ensure this value has at most 1023 characters'
        )

    async def test_null_text(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create(text=None)

        response = await client.put(self.url, json=comment_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'text none is not an allowed value'
        )

    async def test_empty_text(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create(text='')

        response = await client.put(self.url, json=comment_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'text ensure this value has at least 1 characters'
        )

    async def test_invalid_text(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create(text=[1, 2, 3])

        response = await client.put(self.url, json=comment_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'text str type expected'
        )
