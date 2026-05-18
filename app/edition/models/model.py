from app.core.database import Base
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum as Enum


class Edition(Base):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    price: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    isbn: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    specefic_edition_title : Mapped[str] = mapped_column(String, default= None)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class EditionLanguage(Base):
    __tablename__ = "editionlanguage"

    edition_id: Mapped[int] = mapped_column(Integer,ForeignKey("editions.id"),primary_key=True)
    language: Mapped[str] = mapped_column(String,primary_key=True)