from sqlalchemy import Column, ForeignKey, Integer, String, Boolean,BOOLEAN
from database import Base
from enum import Enum as pyEnum
from sqlalchemy.types import Enum as sqlEnum


class Role(str, pyEnum):
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"

class catagory(str, pyEnum):
    SCIENCE = "science"
    ART = "art"
    HISTORY = "history"

class OrderState(str,pyEnum):
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

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(sqlEnum(Role, name="role_enum"), nullable=False, default=Role.USER.value)
    wallet_amount = Column(Integer, nullable=False ,default=0)

    __mapper_args__ = {
        "polymorphic_on": role,
        "polymorphic_identity": "base_user",
    }

class User(BaseUser):
    __tablename__ = "users"

    id = Column(Integer, ForeignKey("base_users.id"), primary_key=True, index=True)
    __mapper_args__ = {
        'polymorphic_identity': Role.USER.value,
    }

class Author(BaseUser):
    __tablename__ = "authors"

    id = Column(Integer, ForeignKey("base_users.id"), primary_key=True, index=True)
    __mapper_args__ = {
        'polymorphic_identity': Role.AUTHOR.value,
    }

class Admin(BaseUser):
    __tablename__ = "admins"
    id = Column(Integer, ForeignKey("base_users.id"), primary_key=True, index=True)
    __mapper_args__ = {
        'polymorphic_identity': Role.ADMIN.value,
    }

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Integer, nullable=False)
    amount = Column(Integer,default= 0, nullable= False)
    category = Column(sqlEnum(catagory, name="catagory_enum"), nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key= True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), index=True)
    state = Column(sqlEnum(OrderState,name = "state_enum"),nullable= False, default=OrderState.WAITFORSELLER.value)
    final_price = Column(Integer, nullable=False)
    date = Column(String, nullable=False)

class ordersbooks(Base):
    __tablename__ = "orders_books"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)

class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)

class transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("base_users.id"), index=True)
    amount = Column(Integer, nullable=False)
    type = Column(sqlEnum(transactionType, name="transaction_type_enum"), nullable=False)
    date = Column(String, nullable=False)