from datetime import datetime

from services.spaces import Space


def validate_space(value: int) -> int:
    Space(value)
    return value


def validate_datetime(value: str) -> datetime | None:
    if not value:
        return None

    if 'T' not in value:
        value += 'T23:59:59.000000'

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise ValueError('invalid isoformat')
