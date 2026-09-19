from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class OutboxEvent:
    id: int | None = None
    event_type: str = ""
    payload: dict[str, Any] | None = None
    processed: bool = False
    created_at: datetime | None = None
