from datetime import date, time
from typing import Any

from services.spaces import Space


def validate_space(value: int) -> int:
    Space(value)
    return value


def validate_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError('invalid isoformat')


def validate_time(value: str) -> time | None:
    if not value:
        return None

    try:
        return time.fromisoformat(value)
    except ValueError:
        raise ValueError('invalid isoformat')


def validate_none(value: Any) -> Any:
    if value is None:
        raise ValueError('none is not an allowed value')
    return value


HEX_COLOR_REGEX = '#[a-fA-F0-9]{6}'
