import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Comment
from tests.api.helpers import serialize_error_response
from tests.api.private.comments.helpers import serialize_comment_response
from tests.factories import CommentDataFactory

pytestmark = [pytest.mark.asyncio]


class TestCreateComment:
    async def _setup(self):
        self.url = app.url_path_for('create_comment')

    async def test_successfully_created(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create()

        response = await client.post(self.url, json=comment_data)

        assert response.status_code == status.HTTP_201_CREATED
        json_response = response.json()
        query = select(Comment).where(Comment.id == json_response['data']['id'])
        comment = await database.fetch_one(query)
        assert comment is not None
        assert json_response == serialize_comment_response(comment)

    async def test_not_authorized(self, anonymous_client):
        await self._setup()
        comment_data = CommentDataFactory.create()

        response = await anonymous_client.post(self.url, json=comment_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_text(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create(text='*' * 1024)

        response = await client.post(self.url, json=comment_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'text ensure this value has at most 1023 characters'
        )

    async def test_null_text(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create(text=None)

        response = await client.post(self.url, json=comment_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'text none is not an allowed value'
        )

    async def test_empty_text(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create(text='')

        response = await client.post(self.url, json=comment_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'text ensure this value has at least 1 characters'
        )

    async def test_invalid_text(self, client):
        await self._setup()
        comment_data = CommentDataFactory.create(text=[1, 2, 3])

        response = await client.post(self.url, json=comment_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'text str type expected'
        )
