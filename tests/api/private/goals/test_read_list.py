import pytest
from fastapi import status

from main import app
from tests.api.helpers import serialize_error_response
from tests.api.private.goals.helpers import serialize_goal_response
from tests.factories import GoalFactory

pytestmark = [pytest.mark.asyncio]


class TestReadGoalList:
    async def _setup(self):
        self.url = app.url_path_for('read_goals_list')

    async def test_successfully_read_list(self, client):
        await self._setup()
        goals = await GoalFactory.create_batch(size=2)

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response(goals)

    async def test_empty_list(self, client):
        await self._setup()
        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response([])

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )

    async def test_search_by_title(self, client):
        await self._setup()
        goal = await GoalFactory.create(title='some TitLe')
        await GoalFactory.create()

        response = await client.get(self.url, params={'search': 'title'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response([goal])

    async def test_filter_archived(self, client):
        await self._setup()
        archived_goal = await GoalFactory.create(archived=True)
        await GoalFactory.create()

        response = await client.get(self.url, params={'archived': True})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response([archived_goal])

    async def test_filter_active(self, client):
        await self._setup()
        await GoalFactory.create(archived=True)
        active_goal = await GoalFactory.create()

        response = await client.get(self.url, params={'archived': False})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response([active_goal])
