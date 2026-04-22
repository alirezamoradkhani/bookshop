from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String, Boolean,DateTime
from sqlalchemy.types import Enum
from app.order.models.enums import OrderState, OrderItemState
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    state: Mapped[OrderState] = mapped_column(Enum(OrderState), default= OrderState.WAITING)
    final_price: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

#order edition is for author to manage their order
class OrderEdition(Base):
    __tablename__ = "orders_editions"

    order_edition_id : Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer,ForeignKey("orders.id"))
    edition_id: Mapped[int] = mapped_column(Integer,ForeignKey("editions.id"))
    state: Mapped[OrderItemState] = mapped_column(Enum(OrderItemState), default=OrderItemState.WAITING)
    last_modify: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    price : Mapped[int] = mapped_column(Integer)