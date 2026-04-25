from dataclasses import dataclass
from app.events.base import BaseEvent


@dataclass
class BorrowCreatedEvent(BaseEvent):
    borrow_id: int 
    edition_id: int
    user_id: int 

    def __post_init__(self):
        self.event_type = "BorrowCreated"


@dataclass
class BorrowReturnedEvent(BaseEvent):
    edition_id: int 
    returned_by: int

    def __post_init__(self):
        self.event_type = "BorrowReturned"


@dataclass
class BorrowOverdueEvent(BaseEvent):
    borrow_id: int
    user_id: int

    def __post_init__(self):
        self.event_type = "BorrowOverdue"