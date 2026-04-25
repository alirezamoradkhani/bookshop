from dataclasses import dataclass
from app.events.base import BaseEvent


@dataclass
class UserCreatedEvent(BaseEvent):
    user_id: int

    def __post_init__(self):
        self.event_type = "UserCreated"