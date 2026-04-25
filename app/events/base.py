from dataclasses import dataclass, field,asdict
from datetime import datetime
import uuid


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(i) for i in obj]
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


@dataclass(kw_only=True)
class BaseEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


def event_to_payload(event) -> dict:
    data = {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "created_at": event.created_at.isoformat(),
    }

    # فقط فیلدهای child event (بدون BaseEvent fields)
    for k, v in event.__dict__.items():
        if k in ("event_id", "event_type", "created_at"):
            continue
        data[k] = make_json_safe(v)

    return data