from app.database import Base
from app.borrow.models.enums import BorrowStatus
from datetime import datetime
from sqlalchemy.types import Enum
from sqlalchemy import Integer,ForeignKey, DateTime
from sqlalchemy.orm import Mapped,mapped_column



class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    edition_id: Mapped[int] = mapped_column(ForeignKey("editions.id"))

    status: Mapped[BorrowStatus] = mapped_column(Enum(BorrowStatus),default= BorrowStatus.ACTIVE)

    borrowed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class Waitlist(Base):
    __tablename__ = "waitlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    edition_id: Mapped[int] = mapped_column(ForeignKey("editions.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))