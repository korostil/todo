from fastapi import status

from main import app
from tests.api.helpers import serialize_error_response
from tests.api.private.goals.helpers import serialize_goal_response
from tests.factories import GoalFactory


class TestReadGoal:
    async def _setup(self):
        self.goal = await GoalFactory.create()
        self.url = app.url_path_for('read_goal', pk=self.goal.id)

    async def test_successfully_read(self, client):
        await self._setup()

        response = await client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response(self.goal)

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('read_goal', pk=pk)

        response = await client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'goal with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
