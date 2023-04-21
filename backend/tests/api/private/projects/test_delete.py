import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Project, Task
from tests.api.helpers import serialize_error_response
from tests.factories import ProjectFactory, TaskFactory

pytestmark = [pytest.mark.asyncio]


class TestDeleteProject:
    async def _setup(self):
        self.project = await ProjectFactory.create()
        self.url = app.url_path_for('delete_project', pk=self.project.id)

    async def test_successfully_deleted(self, client):
        await self._setup()

        response = await client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b''
        query = select(Project).where(Project.id == self.project.id)
        assert await database.fetch_one(query) is None

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('delete_project', pk=pk)

        response = await client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'project with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_linked_tasks(self, client):
        await self._setup()
        await TaskFactory.create_batch(size=2, project_id=self.project.id)

        response = await client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        query = select(Task).where(Task.project_id == self.project.id)
        assert await database.fetch_one(query) is None
