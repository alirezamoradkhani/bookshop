from dataclasses import dataclass
from datetime import datetime

from app.borrow.models.enums import BorrowStatus


@dataclass
class Borrow:
    id: int | None = None
    user_id: int = 0
    edition_id: int = 0
    status: BorrowStatus = BorrowStatus.ACTIVE
    borrowed_at: datetime | None = None
    due_at: datetime | None = None
    returned_at: datetime | None = None
    is_overdue: bool = False


@dataclass
class Waitlist:
    id: int | None = None
    user_id: int = 0
    edition_id: int = 0
    created_at: datetime | None = None
