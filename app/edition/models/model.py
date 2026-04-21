from app.database import Base
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.edition.models.enums import Language
from sqlalchemy.types import Enum as Enum


class Edition(Base):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    price: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    language : Mapped[Language] = mapped_column(Enum(Language, name = "language_enm"))
    specefic_edition_title : Mapped[str] = mapped_column(String, default= None)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)