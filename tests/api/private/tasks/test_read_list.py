import pytest
from fastapi import status

from main import app
from tests.api.helpers import serialize_error_response
from tests.api.private.tasks.helpers import serialize_task_response
from tests.factories import TaskFactory


class TestReadTaskList:
    async def _setup(self):
        self.url = app.url_path_for('read_tasks_list')

    async def test_successfully_read_list(self, client):
        await self._setup()
        tasks = await TaskFactory.create_batch(size=2)

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response(tasks)

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
        project = await TaskFactory.create(title='some TitLe')
        await TaskFactory.create()

        response = await client.get(self.url, params={'search': 'title'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([project])

    async def test_search_by_description(self, client):
        await self._setup()
        project = await TaskFactory.create(description='some DescriPtion')
        await TaskFactory.create()

        response = await client.get(self.url, params={'search': 'description'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_task_response([project])
