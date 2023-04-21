from datetime import datetime

import pytest
from fastapi import status

from main import app
from services.spaces import Space
from tests.api.helpers import serialize_error_response
from tests.api.private.tasks.helpers import serialize_task_response
from tests.factories import ProjectFactory, TaskFactory

pytestmark = [pytest.mark.asyncio]


class TestReadTaskList:
    async def _setup(self):
        self.url = app.url_path_for('read_tasks_list')

    async def test_successfully_read_list(self, client):
        await self._setup()
        tasks = await TaskFactory.create_batch(size=2)

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response(tasks[::-1])

    async def test_empty_list(self, client):
        await self._setup()

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([])

    @pytest.mark.parametrize('completed', [False, True])
    async def test_filter_completed(self, client, completed):
        await self._setup()
        await TaskFactory.create(completed=not completed)
        task = await TaskFactory.create(completed=completed)

        response = await client.get(self.url, params={'completed': completed})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    @pytest.mark.parametrize('decisive', [False, True])
    async def test_filter_decisive(self, client, decisive):
        await self._setup()
        await TaskFactory.create(decisive=not decisive)
        task = await TaskFactory.create(decisive=decisive)

        response = await client.get(self.url, params={'decisive': decisive})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_search_by_title(self, client):
        await self._setup()
        task = await TaskFactory.create(title='some TitLe')
        await TaskFactory.create()

        response = await client.get(self.url, params={'search': 'title'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    async def test_search_by_description(self, client):
        await self._setup()
        task = await TaskFactory.create(description='some DescriPtion')
        await TaskFactory.create()

        response = await client.get(self.url, params={'search': 'description'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    async def test_invalid_due_from(self, client):
        await self._setup()

        response = await client.get(self.url, params={'due_from': 'not a date'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'due_from invalid date format'
        )

    async def test_filter_by_due_from(self, client):
        await self._setup()
        await TaskFactory.create(due_date=datetime(2020, 1, 1))
        task = await TaskFactory.create(due_date=datetime(2020, 1, 2))

        response = await client.get(self.url, params={'due_from': '2020-01-02'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    async def test_filter_by_due_to(self, client):
        await self._setup()
        task = await TaskFactory.create(due_date=datetime(2020, 1, 1))
        await TaskFactory.create(due_date=datetime(2020, 1, 2))

        response = await client.get(self.url, params={'due_to': '2020-01-01'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    @pytest.mark.parametrize(
        'param,value,error_msg',
        [
            ('limit', 51, 'limit ensure this value is less than or equal to 50'),
            ('limit', 0, 'limit ensure this value is greater than 0'),
            ('limit', 'a', 'limit value is not a valid integer'),
            ('offset', -1, 'offset ensure this value is greater than or equal to 0'),
            ('offset', 'a', 'offset value is not a valid integer'),
        ],
        ids=['max-limit', 'min-limit', 'integer-limit', 'min-offset', 'integer-offset'],
    )
    async def test_invalid_limit_offset(self, client, param, value, error_msg):
        await self._setup()

        response = await client.get(self.url, params={param: value})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response('bad_request', error_msg)

    async def test_pagination(self, client):
        await self._setup()
        task = await TaskFactory.create()
        await TaskFactory.create()

        response = await client.get(self.url, params={'limit': 1, 'offset': 1})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    async def test_invalid_project_id(self, client):
        await self._setup()

        response = await client.get(self.url, params={'project_id': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'project_id value is not a valid integer'
        )

    async def test_filter_by_project_id(self, client):
        await self._setup()
        await TaskFactory.create()
        project = await ProjectFactory.create()
        task = await TaskFactory.create(project_id=project.id)

        response = await client.get(self.url, params={'project_id': project.id})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    async def test_filter_by_inbox_project(self, client):
        await self._setup()
        task = await TaskFactory.create()
        project = await ProjectFactory.create()
        await TaskFactory.create(project_id=project.id)

        response = await client.get(self.url, params={'inbox': True})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    async def test_completed_tasks_last(self, client):
        await self._setup()
        completed_task = await TaskFactory.create(completed=True)
        task = await TaskFactory.create()

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task, completed_task])

    async def test_filter_personal_space(self, client):
        await self._setup()
        task = await TaskFactory.create(space=Space.PERSONAL.value)
        await TaskFactory.create()

        response = await client.get(self.url, params={'space': Space.PERSONAL.value})

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == serialize_task_response([task])

    async def test_filter_work_space(self, client):
        await self._setup()
        task = await TaskFactory.create()
        await TaskFactory.create(space=Space.PERSONAL.value)

        response = await client.get(self.url, params={'space': Space.WORK.value})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([task])

    async def test_invalid_space(self, client):
        await self._setup()

        response = await client.get(self.url, params={'space': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space value is not a valid integer'
        )

    async def test_unavailable_space(self, client):
        await self._setup()

        response = await client.get(self.url, params={'space': 100500})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request',
            'space value is not a valid enumeration member; permitted: 1, 2',
        )
