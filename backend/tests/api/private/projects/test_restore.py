import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Project
from tests.api.helpers import serialize_error_response
from tests.api.private.projects.helpers import serialize_project_response
from tests.factories import ProjectFactory

pytestmark = [pytest.mark.asyncio]


class TestRestoreProject:
    async def _setup(self):
        self.project = await ProjectFactory.create()
        self.url = app.url_path_for('restore_project', pk=self.project.id)

    async def test_successfully_archived(self, client):
        await self._setup()

        response = await client.post(self.url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        query = select(Project).where(Project.id == self.project.id)
        project = await database.fetch_one(query)
        assert project.archived_at is None
        assert json_response == serialize_project_response(project)

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('restore_project', pk=pk)

        response = await client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'project with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
