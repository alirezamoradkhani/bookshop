from app.database import Base
from app.transaction.models.enums import TransactionType
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.types import Enum
from sqlalchemy import DateTime
from datetime import datetime


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("base_users.id"))
    amount: Mapped[int] = mapped_column(Integer)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    date: Mapped[datetime] = mapped_column(DateTime)