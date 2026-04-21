from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from enum import Enum as pyEnum
from sqlalchemy.types import Enum as sqlEnum
from sqlalchemy import DateTime
from datetime import datetime

from app.user.models.model import BaseUser, User, Author, Admin
from app.user.models.enums import Role, UserPlan
from app.book.models.enums import Category
from app.book.models.model import Book, BookAuthor
from app.edition.models.enums import Language
from app.edition.models.model import Edition
from app.order.models.enums import OrderState, OrderItemState
from app.order.models.model import Order, OrderEdition


class BorrowStatus(str, pyEnum):
    # WAITING = "waiting"
    ACTIVE = "active"
    OVERDUE = "overdue"
    RETURNED = "returned"
    # CANCELLED = "cancelled"


class TransactionType(str, pyEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    SEND = "send"
    RECEIVE = "receive"


class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    edition_id: Mapped[int] = mapped_column(ForeignKey("editions.id"))

    status: Mapped[BorrowStatus] = mapped_column(sqlEnum(BorrowStatus),default= BorrowStatus.ACTIVE)

    borrowed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Waitlist(Base):
    __tablename__ = "waitlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    edition_id: Mapped[int] = mapped_column(ForeignKey("editions.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("base_users.id"))
    amount: Mapped[int] = mapped_column(Integer)
    type: Mapped[TransactionType] = mapped_column(sqlEnum(TransactionType))
    date: Mapped[str] = mapped_column(String)