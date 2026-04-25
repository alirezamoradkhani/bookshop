from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass(kw_only=True)
class BaseEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)