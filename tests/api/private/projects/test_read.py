import pytest
from fastapi import status

from main import app
from tests.api.helpers import serialize_error_response
from tests.api.private.projects.helpers import serialize_project_response
from tests.factories import ProjectFactory

pytestmark = [pytest.mark.asyncio]


class TestReadProject:
    async def _setup(self):
        self.project = await ProjectFactory.create()
        self.url = app.url_path_for('read_project', pk=self.project.id)

    async def test_successfully_read(self, client):
        await self._setup()

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_project_response(self.project)

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('read_project', pk=pk)

        response = await client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'project with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
