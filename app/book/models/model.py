from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum
from app.database import Base
from app.book.models.enums import Category,Language

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    category: Mapped[Category] = mapped_column(Enum(Category))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)