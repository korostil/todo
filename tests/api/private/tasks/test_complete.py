from datetime import datetime

import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Task
from tests.api.helpers import serialize_error_response
from tests.api.private.tasks.helpers import serialize_task_response
from tests.factories import TaskFactory

pytestmark = [pytest.mark.asyncio]


class TestCompleteTask:
    async def _setup(self):
        self.task = await TaskFactory.create()
        self.url = app.url_path_for('complete_task', pk=self.task.id)

    async def test_successfully_completed(self, client):
        await self._setup()

        response = await client.post(self.url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        query = select(Task).where(Task.id == self.task.id)
        task = await database.fetch_one(query)
        completed_at = task.completed_at.replace(second=0, microsecond=0)
        assert completed_at == datetime.now().replace(second=0, microsecond=0)
        assert json_response == serialize_task_response(task)

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('complete_task', pk=pk)

        response = await client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'task with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
