from sqlalchemy import ForeignKey, Integer, String, Boolean, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from enum import Enum as pyEnum
from sqlalchemy.types import Enum as sqlEnum


class Role(str, pyEnum):
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"

class Category(str, pyEnum):
    SCIENCE = "science"
    ART = "art"
    HISTORY = "history"
    TECHNOLOGY = "technology"
    PROGRAMMING = "programming"
    BUSINESS = "business"
    LITERATURE = "literature"
    PSYCHOLOGY = "psychology"
    PHILOSOPHY = "philosophy"

class OrderState(str, pyEnum):
    WAITFORSELLER = "waitforseller"
    INPROCCES = "inprocces"
    DONE = "done"
    CANCELED = "canceled"

class transactionType(str, pyEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    SEND = "send"
    RECEIVE = "receive"


class BaseUser(Base):
    __tablename__ = "base_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

    role: Mapped[Role] = mapped_column(
        sqlEnum(Role, name="role_enum"),
        nullable=False,
        default=Role.USER
    )

    wallet_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    delete_time: Mapped[str] = mapped_column(String, nullable=True,default=None)

    __mapper_args__ = {
        "polymorphic_on": role,
        "polymorphic_identity": "base_user",
    }


class User(BaseUser):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(ForeignKey("base_users.id"), primary_key=True, index=True)

    __mapper_args__ = {
        'polymorphic_identity': Role.USER.value,
    }


class Author(BaseUser):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(ForeignKey("base_users.id"), primary_key=True, index=True)

    __mapper_args__ = {
        'polymorphic_identity': Role.AUTHOR.value,
    }


class Admin(BaseUser):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(ForeignKey("base_users.id"), primary_key=True, index=True)

    __mapper_args__ = {
        'polymorphic_identity': Role.ADMIN.value,
    }


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    category: Mapped[Category] = mapped_column(
        sqlEnum(Category, name="category_enum"),
        nullable=False
    )
    delete_time: Mapped[str] = mapped_column(String, nullable=True, default=None)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)

    state: Mapped[OrderState] = mapped_column(
        sqlEnum(OrderState, name="state_enum"),
        nullable=False,
        default=OrderState.WAITFORSELLER
    )

    final_price: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)


class ordersbooks(Base):
    __tablename__ = "orders_books"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)


class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)


class transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_users.id"), index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    type: Mapped[transactionType] = mapped_column(
        sqlEnum(transactionType, name="transaction_type_enum"),
        nullable=False
    )

    date: Mapped[str] = mapped_column(String, nullable=False)