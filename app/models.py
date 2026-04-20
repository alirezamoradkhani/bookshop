from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from enum import Enum as pyEnum
from sqlalchemy.types import Enum as sqlEnum
from sqlalchemy import DateTime
from datetime import datetime


from app.user.models.enums import Role, UserPlan

class Category(str, pyEnum):
    SCIENCE = "science"
    ART = "art"
    HISTORY = "history"
    TECHNOLOGY = "technology"
    PROGRAMMING = "programming"
    BUSINESS = "business"
    LITERATURE = "literature"

class Language(str,pyEnum):
    FA = "fa"
    EN = "en"
    ARB = "arb"
    

class OrderState(str, pyEnum):
    WAITING = "waiting"
    IN_PROCCESE = "in_proccese"
    DONE = "done"
    CANCELED = "canceled"

class OrderItemState(str, pyEnum):
    WAITING = "waiting"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PREPARING = "preparing"
    DONE = "done"

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


from app.user.models.model import BaseUser, User, Author, Admin

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    category: Mapped[Category] = mapped_column(sqlEnum(Category))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class Edition(Base):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    price: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    language : Mapped[Language] = mapped_column(sqlEnum(Language, name = "language_enm"))
    specefic_edition_title : Mapped[str] = mapped_column(String, default= None)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)


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



class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    state: Mapped[OrderState] = mapped_column(sqlEnum(OrderState), default= OrderState.WAITING)
    final_price: Mapped[int] = mapped_column(Integer)
    date: Mapped[str] = mapped_column(String)


class OrderEdition(Base):
    __tablename__ = "orders_editions"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    edition_id: Mapped[int] = mapped_column(ForeignKey("editions.id"), primary_key=True)
    state: Mapped[OrderItemState] = mapped_column(sqlEnum(OrderItemState), default=OrderItemState.WAITING)

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("base_users.id"))
    amount: Mapped[int] = mapped_column(Integer)
    type: Mapped[TransactionType] = mapped_column(sqlEnum(TransactionType))
    date: Mapped[str] = mapped_column(String)