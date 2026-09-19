from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


def serialize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return serialize(asdict(value))
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value
