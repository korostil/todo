import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Task
from tests.api.helpers import serialize_error_response
from tests.api.private.tasks.helpers import serialize_task_response
from tests.factories import ProjectFactory, TaskDataFactory

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

        response = await anonymous_client.post(self.url, json={})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(title='*' * 256)

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_title_required(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        del task_data['title']

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title field required'
        )

    async def test_null_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(title=None)

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_empty_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(title='')

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(title=[1, 2, 3])

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )

    async def test_too_long_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(description='*' * 256)

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at most 255 characters'
        )

    async def test_description_field_not_required(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        del task_data['description']

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_201_CREATED

    async def test_null_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(description=None)

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_201_CREATED

    async def test_empty_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(description='')

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at least 1 characters'
        )

    async def test_invalid_description(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(description=[1, 2, 3])

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description str type expected'
        )

    async def test_invalid_due_date(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(due_date='2020/1/1')

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'due_date invalid isoformat'
        )

    async def test_invalid_due_time(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(due_time='1/1/1')

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'due_time invalid isoformat'
        )

    async def test_due_date(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(due_date='2020-01-01', due_time=None)

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()['data']
        assert data['due_date'] == '2020-01-01'
        assert data['due_time'] is None

    async def test_due_time(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(due_date=None, due_time='10:00')

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()['data']
        assert data['due_date'] is None
        assert data['due_time'] == '10:00:00'

    async def test_due_date_and_time(self, client):
        await self._setup()
        expected_due_date = '2020-01-01'
        expected_due_time = '10:00:00'
        task_data = TaskDataFactory.create(
            due_date=expected_due_date, due_time=expected_due_time
        )

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()['data']
        assert data['due_date'] == expected_due_date
        assert data['due_time'] == expected_due_time

    async def test_no_due(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        del task_data['due_date']
        del task_data['due_time']

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()['data']
        assert data['due_date'] is None
        assert data['due_time'] is None

    async def test_invalid_space(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(space='invalid')

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space value is not a valid integer'
        )

    async def test_null_space(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(space=None)

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space none is not an allowed value'
        )

    async def test_space_required(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        del task_data['space']

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space field required'
        )

    async def test_unavailable_space(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(space=1000)

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space 1000 is not a valid Space'
        )

    async def test_default_decisive(self, client):
        await self._setup()
        task_data = TaskDataFactory.create()
        del task_data['decisive']

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_201_CREATED

    async def test_invalid_decisive(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(decisive='invalid')

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'decisive value could not be parsed to a boolean'
        )

    async def test_null_decisive(self, client):
        await self._setup()
        task_data = TaskDataFactory.create(decisive=None)

        response = await client.post(self.url, json=task_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'decisive none is not an allowed value'
        )

    async def test_link_project(self, client):
        await self._setup()
        project = await ProjectFactory.create()
        project_data = TaskDataFactory.create(project_id=project.id)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['data']['project_id'] == project.id

    async def test_project_not_found(self, client):
        await self._setup()
        pk = 100500
        project_data = TaskDataFactory.create(project_id=pk)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'project with pk={pk} not found'
        )

    async def test_invalid_project(self, client):
        await self._setup()
        project_data = TaskDataFactory.create(project_id='invalid')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'project_id value is not a valid integer'
        )
