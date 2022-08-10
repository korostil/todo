import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Project
from tests.api.helpers import serialize_error_response
from tests.api.private.projects.helpers import serialize_project_response
from tests.factories import ProjectDataFactory, ProjectFactory

pytestmark = [pytest.mark.asyncio]


class TestUpdateProject:
    async def _setup(self):
        self.project = await ProjectFactory.create()
        self.url = app.url_path_for('update_project', pk=self.project.id)

    async def test_successfully_updated(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_200_OK
        query = select(Project).where(Project.id == self.project.id)
        project = await database.fetch_one(query)
        assert project is not None
        assert response.json() == serialize_project_response(project)

    async def test_partially_updated(self, client):
        await self._setup()
        expected_title = 'updated-title'
        project_data = {'title': expected_title}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['title'] == expected_title

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('update_project', pk=pk)

        response = await client.put(url, json={})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'project with pk={pk} not found'
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
        project_data = {'title': '*' * 256}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_null_title(self, client):
        await self._setup()
        project_data = {'title': None}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_empty_title(self, client):
        await self._setup()
        project_data = {'title': ''}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        project_data = {'title': [1, 2, 3]}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )

    async def test_too_long_description(self, client):
        await self._setup()
        project_data = {'description': '*' * 256}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at most 255 characters'
        )

    async def test_null_description(self, client):
        await self._setup()
        project_data = {'description': None}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description none is not an allowed value'
        )

    async def test_empty_description(self, client):
        await self._setup()
        project_data = {'description': ''}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at least 1 characters'
        )

    async def test_invalid_description(self, client):
        await self._setup()
        project_data = {'description': [1, 2, 3]}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description str type expected'
        )

    async def test_invalid_space(self, client):
        await self._setup()
        project_data = {'space': 'invalid'}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space value is not a valid integer'
        )

    async def test_null_space(self, client):
        await self._setup()
        project_data = {'space': None}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space None is not a valid Space'
        )

    async def test_unavailable_space(self, client):
        await self._setup()
        project_data = {'space': 1000}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space 1000 is not a valid Space'
        )
