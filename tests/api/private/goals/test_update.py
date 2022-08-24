from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Goal
from tests.api.helpers import serialize_error_response
from tests.api.private.goals.helpers import serialize_goal_response
from tests.factories import GoalDataFactory, GoalFactory


class TestUpdateGoal:
    async def _setup(self):
        self.goal = await GoalFactory.create()
        self.url = app.url_path_for('update_goal', pk=self.goal.id)

    async def test_successfully_updated(self, client):
        await self._setup()
        goal_data = GoalDataFactory.create()

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_200_OK
        query = select(Goal).where(Goal.id == self.goal.id)
        goal = await database.fetch_one(query)
        assert goal is not None
        assert response.json() == serialize_goal_response(goal)

    async def test_partially_updated(self, client):
        await self._setup()
        expected_title = 'updated-title'
        goal_data = {'title': expected_title}

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['title'] == expected_title

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('update_goal', pk=pk)

        response = await client.put(url, json={})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'goal with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.put(self.url, json={})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_too_long_title(self, client):
        await self._setup()
        goal_data = {'title': '*' * 256}

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at most 255 characters'
        )

    async def test_null_title(self, client):
        await self._setup()
        goal_data = {'title': None}

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title none is not an allowed value'
        )

    async def test_empty_title(self, client):
        await self._setup()
        goal_data = {'title': ''}

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title ensure this value has at least 1 characters'
        )

    async def test_invalid_title(self, client):
        await self._setup()
        goal_data = {'title': [1, 2, 3]}

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'title str type expected'
        )

    async def test_invalid_week(self, client):
        await self._setup()
        goal_data = {'week': 'invalid'}

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'week value is not a valid integer'
        )

    async def test_invalid_month(self, client):
        await self._setup()
        goal_data = {'month': 'invalid'}

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'month value is not a valid integer'
        )

    async def test_invalid_year(self, client):
        await self._setup()
        goal_data = {'year': 'invalid'}

        response = await client.put(self.url, json=goal_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'year value is not a valid integer'
        )

    async def test_invalid_status(self, client):
        await self._setup()
        project_data = {'status': 'invalid'}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'status value is not a valid integer'
        )

    async def test_null_status(self, client):
        await self._setup()
        project_data = {'status': None}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'status None is not a valid Status'
        )

    async def test_unavailable_status(self, client):
        await self._setup()
        project_data = {'status': 1000}

        response = await client.put(self.url, json=project_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'status 1000 is not a valid Status'
        )
