import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Goal, Status
from tests.api.helpers import serialize_error_response
from tests.api.private.goals.helpers import serialize_goal_response
from tests.factories import GoalDataFactory

pytestmark = [pytest.mark.asyncio]


class TestCreateGoal:
    async def _setup(self):
        self.url = app.url_path_for('create_goal')

    async def test_successfully_created(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create()

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_201_CREATED
        json_response = response.json()
        query = select(Goal).where(Goal.id == json_response['data']['id'])
        goal = await database.fetch_one(query)
        assert goal is not None
        assert json_response == serialize_goal_response(goal)

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.post(self.url, json={})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create(title='*' * 256)

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_title_required(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create()
        del goal_data['title']

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title field required'
        )

    async def test_null_title(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create(title=None)

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_empty_title(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create(title='')

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create(title=[1, 2, 3])

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )

    async def test_invalid_week(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create(week='invalid')

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'week value is not a valid integer'
        )

    async def test_invalid_month(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create(month='invalid')

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'month value is not a valid integer'
        )

    async def test_invalid_year(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create(year='invalid')

        response = await client.post(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'year value is not a valid integer'
        )

    async def test_invalid_status(self, client):
        await self._setup()
        project_data = GoalDataFactory.create(status='invalid')

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'status value is not a valid integer'
        )

    async def test_default_status(self, client):
        await self._setup()
        project_data = GoalDataFactory.create(status=None)
        del project_data['status']

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['data']['status'] == Status.NEW.value

    async def test_unavailable_status(self, client):
        await self._setup()
        project_data = GoalDataFactory.create(status=1000)

        response = await client.post(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'status 1000 is not a valid Status'
        )
