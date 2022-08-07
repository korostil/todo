from collections.abc import Callable

from databases.interfaces import Record


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
