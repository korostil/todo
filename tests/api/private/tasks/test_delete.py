import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Task
from tests.api.helpers import serialize_error_response
from tests.factories import TaskFactory

pytestmark = [pytest.mark.asyncio]


class TestDeleteTask:
    async def _setup(self):
        self.task = await TaskFactory.create()
        self.url = app.url_path_for('delete_task', pk=self.task.id)

    async def test_successfully_deleted(self, client):
        await self._setup()

        response = await client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b''
        query = select(Task).where(Task.id == self.task.id)
        assert await database.fetch_one(query) is None

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('delete_task', pk=pk)

        response = await client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'task with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
