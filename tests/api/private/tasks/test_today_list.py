from datetime import datetime, timedelta

import pytest
from fastapi import status

from main import app
from tests.api.helpers import serialize_error_response
from tests.api.private.tasks.helpers import serialize_task_response
from tests.factories import TaskFactory

pytestmark = [pytest.mark.asyncio]


class TestReadTodayList:
    async def _setup(self):
        self.url = app.url_path_for('today_tasks')

    async def test_successfully_today_list(self, client):
        await self._setup()
        today = datetime.today()
        tasks = await TaskFactory.create_batch(size=2, created_at=today)
        await TaskFactory.create(created_at=today - timedelta(days=1))

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response(tasks)

    async def test_empty_list(self, client):
        await self._setup()
        await TaskFactory.create(created_at=datetime.today() - timedelta(days=1))

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([])

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
