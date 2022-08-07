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

    async def test_not_found(self, client):
        await self._setup()
        pk = 100500
        project_data = ProjectDataFactory.create()
        url = app.url_path_for('update_project', pk=pk)

        response = await client.put(url, json=project_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'project with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()
        project_data = ProjectDataFactory.create()

        response = await anonymous_client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()
        project_data['title'] = '*' * 256

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_too_long_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()
        project_data['description'] = '*' * 256

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at most 255 characters'
        )
