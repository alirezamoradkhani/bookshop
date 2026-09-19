from dataclasses import dataclass
from datetime import datetime

from app.order.models.enums import OrderItemState, OrderState


@dataclass
class Order:
    id: int | None = None
    user_id: int = 0
    state: OrderState = OrderState.WAITING
    final_price: int = 0
    date: datetime | None = None


@dataclass
class OrderEdition:
    order_edition_id: int | None = None
    order_id: int = 0
    edition_id: int = 0
    state: OrderItemState = OrderItemState.WAITING
    last_modify: datetime | None = None
    price: int = 0

    @property
    def id(self) -> int | None:
        return self.order_edition_id
