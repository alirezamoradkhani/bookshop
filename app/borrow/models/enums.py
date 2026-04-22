from enum import Enum

class BorrowStatus(str, Enum):
    # WAITING = "waiting"
    ACTIVE = "active"
    OVERDUE = "overdue"
    RETURNED = "returned"
    # CANCELLED = "cancelled"