from services.spaces import Space


def validate_space(value: int) -> int:
    Space(value)
    return value
