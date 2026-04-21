from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.types import Enum
from app.order.models.enums import OrderState, OrderItemState


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    state: Mapped[OrderState] = mapped_column(Enum(OrderState), default= OrderState.WAITING)
    final_price: Mapped[int] = mapped_column(Integer)
    date: Mapped[str] = mapped_column(String)

#order edition is for author to manage their order
class OrderEdition(Base):
    __tablename__ = "orders_editions"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    edition_id: Mapped[int] = mapped_column(ForeignKey("editions.id"), primary_key=True)
    state: Mapped[OrderItemState] = mapped_column(Enum(OrderItemState), default=OrderItemState.WAITING)