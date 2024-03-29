import pytest
from fastapi import status

from main import app
from services.spaces import Space
from tests.api.helpers import serialize_error_response
from tests.api.private.projects.helpers import serialize_project_response
from tests.factories import ProjectFactory

pytestmark = [pytest.mark.asyncio]


class TestReadProjectList:
    async def _setup(self):
        self.url = app.url_path_for('read_projects_list')

    async def test_successfully_read_list(self, client):
        await self._setup()
        projects = await ProjectFactory.create_batch(size=2)

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response(projects)

    async def test_filter_archived(self, client):
        await self._setup()
        archived_project = await ProjectFactory.create(archived=True)
        await ProjectFactory.create()

        response = await client.get(self.url, params={'archived': True})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response([archived_project])

    async def test_filter_active(self, client):
        await self._setup()
        await ProjectFactory.create(archived=True)
        active_project = await ProjectFactory.create()

        response = await client.get(self.url, params={'archived': False})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response([active_project])

    async def test_empty_list(self, client):
        await self._setup()

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response([])

    async def test_invalid_archived(self, client):
        await self._setup()

        response = await client.get(self.url, params={'archived': 'invalid'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'archived value could not be parsed to a boolean'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_search_by_title(self, client):
        await self._setup()
        project = await ProjectFactory.create(title='some TitLe')
        await ProjectFactory.create()

        response = await client.get(self.url, params={'search': 'title'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response([project])

    async def test_search_by_description(self, client):
        await self._setup()
        project = await ProjectFactory.create(description='some DescriPtion')
        await ProjectFactory.create()

        response = await client.get(self.url, params={'search': 'description'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response([project])

    async def test_filter_personal_space(self, client):
        await self._setup()
        project = await ProjectFactory.create(space=Space.PERSONAL.value)
        await ProjectFactory.create()

        response = await client.get(self.url, params={'space': Space.PERSONAL.value})

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == serialize_project_response([project])

    async def test_filter_work_space(self, client):
        await self._setup()
        project = await ProjectFactory.create()
        await ProjectFactory.create(space=Space.PERSONAL.value)

        response = await client.get(self.url, params={'space': Space.WORK.value})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response([project])

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
