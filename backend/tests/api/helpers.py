from collections.abc import Callable

import pytest
from databases.interfaces import Record
from factory import Factory
from starlette import status

from main import app


def serialize_response(
    instance: Record | list | None = None, *, serializer: Callable = lambda x: {}
) -> dict:
    data = None
    kwargs = {}

    if isinstance(instance, list):
        data = [{'id': item.id, **serializer(item)} for item in instance]
        kwargs['count'] = len(instance)
    elif isinstance(instance, Record):
        data = {'id': instance.id, **serializer(instance)}

    return {'status': 'ok', 'data': data, **kwargs}


def serialize_error_response(code: str, message: str) -> dict[str, str]:
    return {'status': 'error', 'error': {'code': code, 'message': message}}


class RestfulEndpoint:
    entity_name: str
    factory: Factory
    orm_factory: Factory
    data_factory: Factory
    request_factory: Factory
    serialize_response_method: Callable
    version: int

    @pytest.fixture(autouse=True)
    def setup(self):
        self.create_path = f'read_{self.entity_name}'
        self.read_path = f'read_{self.entity_name}'
        self.url_read_list = f'read_{self.entity_name}_list'

    async def test_read_successfully(self, client):
        entity = await self.orm_factory.create()
        url = app.url_path_for(self.url_read, pk=entity.pk)

        response = await client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.serialize_response_method(entity)

    async def test_read_not_found(self, client):
        pk = 100500
        url = app.url_path_for('read_task', pk=pk)

        response = await client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == serialize_error_response(
            'not_found', f'task with pk={pk} not found'
        )

    async def test_not_authorized(self, anonymous_client):
        await self._setup()

        response = await anonymous_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == serialize_error_response(
            'forbidden', 'Not authenticated'
        )
