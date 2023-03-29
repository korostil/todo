from datetime import datetime

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

    async def test_filter_achieved(self, client):
        await self._setup()
        achieved_goal = await GoalFactory.create(achieved=True)
        await GoalFactory.create()

        response = await client.get(self.url, params={'achieved': True})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response([achieved_goal])

    async def test_filter_active(self, client):
        await self._setup()
        await GoalFactory.create(achieved=True)
        active_goal = await GoalFactory.create()

        response = await client.get(self.url, params={'achieved': False})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response([active_goal])

    async def test_last_year(self, client):
        await self._setup()
        last_year = datetime.now().year - 1

        response = await client.get(self.url, params={'year': last_year})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request',
            f'year ensure this value is greater than or equal to {last_year + 1}',
        )

    async def test_invalid_year(self, client):
        await self._setup()

        response = await client.get(self.url, params={'year': 'invalid'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'year value is not a valid integer'
        )

    async def test_invalid_month(self, client):
        await self._setup()

        response = await client.get(self.url, params={'month': 'invalid'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'month value is not a valid integer'
        )

    @pytest.mark.parametrize(
        'month,err_msg',
        [
            (0, 'month ensure this value is greater than or equal to 1'),
            (13, 'month ensure this value is less than or equal to 12'),
        ],
    )
    async def test_out_of_range_month(self, client, month, err_msg):
        await self._setup()

        response = await client.get(self.url, params={'month': month})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response('bad_request', err_msg)

    async def test_month_without_year(self, client):
        await self._setup()

        response = await client.get(self.url, params={'month': 1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serialize_error_response(
            'bad_request', 'Request should contain both the year and month'
        )

    async def test_filter_by_year(self, client):
        await self._setup()
        year = datetime.now().year
        await GoalFactory.create(year=year, month=1)
        goal = await GoalFactory.create(year=year)

        response = await client.get(self.url, params={'year': year})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response([goal])

    async def test_filter_by_month_and_year(self, client):
        await self._setup()
        year = datetime.now().year
        await GoalFactory.create(year=year)
        goal = await GoalFactory.create(year=year, month=1)

        response = await client.get(self.url, params={'year': year, 'month': 1})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serialize_goal_response([goal])
