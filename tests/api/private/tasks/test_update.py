from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Task
from tests.api.helpers import serialize_error_response
from tests.api.private.tasks.helpers import serialize_task_response
from tests.factories import TaskDataFactory, TaskFactory


class TestUpdateTask:
    async def _setup(self):
        self.task = await TaskFactory.create()
        self.url = app.url_path_for('update_task', pk=self.task.id)

    async def test_successfully_updated(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()

        response = await client.put(self.url, json=task_data)

        assert response.status_code == status.HTTP_200_OK
        query = select(Task).where(Task.id == self.task.id)
        task = await database.fetch_one(query)
        assert task is not None
        assert response.json() == serialize_task_response(task)

    async def test_partially_updated(self, client):
        await self._setup()
        expected_title = 'updated-title'
        task_data = {'title': expected_title}

        response = await client.put(self.url, json=task_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['title'] == expected_title

    async def test_not_found(self, client):
        await self._setup()
        pk = 100500
        task_data = TaskDataFactory.create()
        url = app.url_path_for('update_task', pk=pk)

        response = await client.put(url, json=task_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'task with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()
        task_data = TaskDataFactory.create()

        response = await anonymous_client.put(self.url, json=task_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['title'] = '*' * 256

        response = await client.put(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_too_long_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['description'] = '*' * 256

        response = await client.put(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at most 255 characters'
        )

    async def test_invalid_space(self, client):
        await self._setup()
        task_data = {'space': 'invalid'}

        response = await client.put(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space value is not a valid integer'
        )

    async def test_null_space(self, client):
        await self._setup()
        task_data = {'space': None}

        response = await client.put(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space None is not a valid Space'
        )

    async def test_unavailable_space(self, client):
        await self._setup()
        task_data = {'space': 1000}

        response = await client.put(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space 1000 is not a valid Space'
        )
