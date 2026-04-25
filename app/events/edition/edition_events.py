from dataclasses import dataclass
from app.events.base import BaseEvent


@dataclass
class EditionCreatedEvent(BaseEvent):
    edition_id: int

    def __post_init__(self):
        self.event_type = "EditionCreated"


@dataclass
class EditionUpdatedEvent(BaseEvent):
    edition_id: int

    def __post_init__(self):
        self.event_type = "EditionUpdated"


@dataclass
class EditionDeletedEvent(BaseEvent):
    edition_id: int

    def __post_init__(self):
        self.event_type = "EditionDeleted"