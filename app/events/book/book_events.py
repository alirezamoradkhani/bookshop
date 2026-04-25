from dataclasses import dataclass
from app.events.base import BaseEvent


@dataclass
class BookCreatedEvent(BaseEvent):
    book_id: int

    def __post_init__(self):
        self.event_type = "BookCreated"


@dataclass
class BookUpdatedEvent(BaseEvent):
    book_id: int

    def __post_init__(self):
        self.event_type = "BookUpdated"


@dataclass
class BookDeletedEvent(BaseEvent):
    book_id: int

    def __post_init__(self):
        self.event_type = "BookDeleted"