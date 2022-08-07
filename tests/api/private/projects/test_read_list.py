import pytest
from fastapi import status

from main import app
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

    @pytest.mark.parametrize('archived', [False, True])
    async def test_filter_by_archived(self, client, archived):
        await self._setup()
        projects = await ProjectFactory.create_batch(size=2, archived=archived)

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response(projects)

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
