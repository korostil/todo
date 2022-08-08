import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Task
from tests.api.helpers import serialize_error_response
from tests.api.private.tasks.helpers import serialize_task_response
from tests.factories import TaskDataFactory

pytestmark = [pytest.mark.asyncio]


class TestCreateTask:
    async def _setup(self):
        self.url = app.url_path_for('create_task')

    async def test_successfully_created(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_201_CREATED
        json_response = response.json()
        query = select(Task).where(Task.id == json_response['data']['id'])
        task = await database.fetch_one(query)
        assert task is not None
        assert json_response == serialize_task_response(task)

    async def test_not_authorized(self, anonymous_client):
        await self._setup()
        task_data = TaskDataFactory.create()

        response = await anonymous_client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['title'] = '*' * 256

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_null_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['title'] = None

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_empty_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['title'] = ''

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['title'] = [1, 2, 3]

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )

    async def test_too_long_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['description'] = '*' * 256

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at most 255 characters'
        )

    async def test_null_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['description'] = None

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description none is not an allowed value'
        )

    async def test_empty_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['description'] = ''

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at least 1 characters'
        )

    async def test_empty_due(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['due'] = ''

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'due invalid datetime format'
        )

    @pytest.mark.xfail
    async def test_due_date(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(due='2020-01-01')

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['due'] == '2020-01-01 00:00:00'

    async def test_invalid_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        task_data['description'] = [1, 2, 3]

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description str type expected'
        )
