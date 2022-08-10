import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Tag
from tests.api.helpers import serialize_error_response
from tests.api.private.tags.helpers import serialize_tag_response
from tests.factories import TagDataFactory

pytestmark = [pytest.mark.asyncio]


class TestCreateTag:
    async def _setup(self):
        self.url = app.url_path_for('create_tag')

    async def test_successfully_created(self, client):
        await self._setup()
        tag_data = TagDataFactory.create()

        response = await client.post(self.url, json=tag_data)

        assert response.status_code == status.HTTP_201_CREATED
        json_response = response.json()
        query = select(Tag).where(Tag.id == json_response['data']['id'])
        tag = await database.fetch_one(query)
        assert tag is not None
        assert json_response == serialize_tag_response(tag)

    async def test_not_authorized(self, anonymous_client):
        await self._setup()
        tag_data = TagDataFactory.create()

        response = await anonymous_client.post(self.url, json=tag_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        tag_data = TagDataFactory.create(title='*' * 32)

        response = await client.post(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 31 characters'
        )

    async def test_null_title(self, client):
        await self._setup()
        tag_data = TagDataFactory.create(title=None)

        response = await client.post(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_empty_title(self, client):
        await self._setup()
        tag_data = TagDataFactory.create(title='')

        response = await client.post(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        tag_data = TagDataFactory.create(title=[1, 2, 3])

        response = await client.post(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )
