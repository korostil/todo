from datetime import datetime

import pytest
from fastapi import status
from sqlalchemy import select

from app.database import database
from main import app
from models import Goal
from tests.api.helpers import serialize_error_response
from tests.api.private.goals.helpers import serialize_goal_response
from tests.factories import GoalFactory

pytestmark = [pytest.mark.asyncio]


class TestArchiveGoal:
    async def _setup(self):
        self.goal = await GoalFactory.create()
        self.url = app.url_path_for('archive_goal', pk=self.goal.id)

    async def test_successfully_archived(self, client):
        await self._setup()

        response = await client.post(self.url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        query = select(Goal).where(Goal.id == self.goal.id)
        goal = await database.fetch_one(query)
        archived_at = goal.archived_at.replace(second=0, microsecond=0)
        assert archived_at == datetime.now().replace(second=0, microsecond=0)
        assert json_response == serialize_goal_response(goal)

    async def test_not_found(self, client):
        pk = 100500
        url = app.url_path_for('archive_goal', pk=pk)

        response = await client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'goal with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
