import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Tag
from tests.api.helpers import serialize_error_response
from tests.api.private.tags.helpers import serialize_tag_response
from tests.factories import TagDataFactory, TagFactory


class TestUpdateTag:
    async def _setup(self):
        self.tag = await TagFactory.create()
        self.url = app.url_path_for('update_tag', pk=self.tag.id)

    async def test_successfully_updated(self, client):
        await self._setup()
        tag_data = TagDataFactory.create()

        response = await client.put(self.url, json=tag_data)

        assert response.status_code == status.HTTP_200_OK
        query = select(Tag).where(Tag.id == self.tag.id)
        tag = await database.fetch_one(query)
        assert tag is not None
        assert response.json() == serialize_tag_response(tag)

    async def test_partially_updated(self, client):
        await self._setup()
        expected_title = 'updated-title'
        tag_data = {'title': expected_title}

        response = await client.put(self.url, json=tag_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['title'] == expected_title

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('update_tag', pk=pk)

        response = await client.put(url, json={})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'tag with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.put(self.url, json={})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        tag_data = {'title': '*' * 32}

        response = await client.put(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 31 characters'
        )

    async def test_null_title(self, client):
        await self._setup()
        tag_data = {'title': None}

        response = await client.put(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_empty_title(self, client):
        await self._setup()
        tag_data = {'title': ''}

        response = await client.put(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        tag_data = {'title': [1, 2, 3]}

        response = await client.put(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )

    async def test_invalid_color_type(self, client):
        await self._setup()
        tag_data = {'color': ['1'] * 6}

        response = await client.put(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'color str type expected'
        )

    @pytest.mark.parametrize(
        'color', ['RRRRRR', 'FFF'], ids=['out_of_range', 'too_short']
    )
    async def test_invalid_color(self, client, color):
        await self._setup()
        tag_data = {'color': color}

        response = await client.put(self.url, json=tag_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'color string does not match regex "[a-fA-F0-9]{6}"'
        )

    async def test_null_color(self, client):
        await self._setup()
        response = await client.put(self.url, json={'color': None})
        assert response.status_code == status.HTTP_200_OK
