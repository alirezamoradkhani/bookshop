from dataclasses import dataclass
from datetime import datetime

from app.transaction.models.enums import TransactionType


@dataclass
class Transaction:
    id: int | None = None
    user_id: int = 0
    amount: int = 0
    type: TransactionType = TransactionType.DEPOSIT
    date: datetime | None = None
