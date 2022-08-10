import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Project
from tests.api.helpers import serialize_error_response
from tests.api.private.projects.helpers import serialize_project_response
from tests.factories import ProjectDataFactory

pytestmark = [pytest.mark.asyncio]


class TestCreateProject:
    async def _setup(self):
        self.url = app.url_path_for('create_project')

    async def test_successfully_created(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_201_CREATED
        json_response = response.json()
        query = select(Project).where(Project.id == json_response['data']['id'])
        project = await database.fetch_one(query)
        assert project is not None
        assert json_response == serialize_project_response(project)

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.post(self.url, json={})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(title='*' * 256)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_null_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(title=None)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_title_required(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()
        del project_data['title']

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title field required'
        )

    async def test_empty_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(title='')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(title=[1, 2, 3])

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )

    async def test_too_long_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(description='*' * 256)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at most 255 characters'
        )

    async def test_null_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(description=None)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description none is not an allowed value'
        )

    async def test_description_required(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()
        del project_data['description']

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description field required'
        )

    async def test_empty_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(description='')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at least 1 characters'
        )

    async def test_invalid_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(description=[1, 2, 3])

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description str type expected'
        )

    async def test_invalid_space(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(space='invalid')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space value is not a valid integer'
        )

    async def test_null_space(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(space=None)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space none is not an allowed value'
        )

    async def test_space_required(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()
        del project_data['space']

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space field required'
        )

    async def test_unavailable_space(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(space=1000)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space 1000 is not a valid Space'
        )
