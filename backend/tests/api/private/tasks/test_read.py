import pytest
from fastapi import status

from main import app
from tests.api.helpers import serialize_error_response
from tests.api.private.tasks.helpers import serialize_task_response
from tests.factories import TaskFactory

pytestmark = [pytest.mark.asyncio]


class TestReadTask:
    async def _setup(self):
        self.task = await TaskFactory.create()
        self.url = app.url_path_for('read_task', pk=self.task.id)

    async def test_successfully_read(self, client):
        await self._setup()

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response(self.task)

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('read_task', pk=pk)

        response = await client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'task with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
