import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Project
from tests.api.helpers import serialize_error_response
from tests.api.private.projects.helpers import serialize_project_response
from tests.factories import GoalFactory, ProjectDataFactory

pytestmark = [pytest.mark.asyncio]


class TestCreateProject:
    async def _setup(self):
        self.url = app.url_path_for('create_project')

    async def test_successfully_created(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_201_CREATED
        json_response = response.json()
        query = select(Project).where(Project.id == json_response['data']['id'])
        project = await database.fetch_one(query)
        assert project is not None
        assert json_response == serialize_project_response(project)

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.post(self.url, json={})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(title='*' * 256)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_null_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(title=None)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_title_required(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()
        del project_data['title']

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title field required'
        )

    async def test_empty_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(title='')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(title=[1, 2, 3])

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )

    async def test_too_long_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(description='*' * 256)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at most 255 characters'
        )

    async def test_null_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(description=None)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description none is not an allowed value'
        )

    async def test_description_required(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()
        del project_data['description']

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description field required'
        )

    async def test_empty_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(description='')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description ensure this value has at least 1 characters'
        )

    async def test_invalid_description(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(description=[1, 2, 3])

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'description str type expected'
        )

    async def test_invalid_space(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(space='invalid')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space value is not a valid integer'
        )

    async def test_null_space(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(space=None)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space none is not an allowed value'
        )

    async def test_space_required(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create()
        del project_data['space']

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space field required'
        )

    async def test_unavailable_space(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(space=1000)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'space 1000 is not a valid Space'
        )

    async def test_invalid_color_type(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(color=['1'] * 6)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'color str type expected'
        )

    @pytest.mark.parametrize(
        'color',
        ['#RRRRRR', '#FFF', 'FFFFFF'],
        ids=['out_of_range', 'too_short', 'not_starts_with_hash'],
    )
    async def test_invalid_color(self, client, color):
        await self._setup()
        project_data = ProjectDataFactory.create(color=color)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'color string does not match regex "#[a-fA-F0-9]{6}"'
        )

    async def test_null_color(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(color=None)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_201_CREATED

    async def test_link_goal(self, client):
        await self._setup()
        goal = await GoalFactory.create()
        project_data = ProjectDataFactory.create(goal_id=goal.id)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['data']['goal_id'] == goal.id

    async def test_goal_not_found(self, client):
        await self._setup()
        pk = 100500
        project_data = ProjectDataFactory.create(goal_id=pk)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'goal with pk={pk} not found'
        )

    async def test_invalid_goal(self, client):
        await self._setup()
        project_data = ProjectDataFactory.create(goal_id='invalid')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'goal_id value is not a valid integer'
        )
