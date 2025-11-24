import os


def str_to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def to_int(env_name: str, default: int) -> int:
    val = os.getenv(env_name)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return default


def to_float(env_name: str, default: float) -> float:
    val = os.getenv(env_name)
    if val is None:
        return default
    try:
        return float(val)
    except ValueError:
        return default
