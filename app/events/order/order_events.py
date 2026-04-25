from dataclasses import dataclass
from app.events.base import BaseEvent


@dataclass
class OrderCreatedEvent(BaseEvent):
    order_id: int

    def __post_init__(self):
        self.event_type = "OrderCreated"


@dataclass
class OrderCanceledEvent(BaseEvent):
    order_id: int 

    def __post_init__(self):
        self.event_type = "OrderCanceled"


@dataclass
class OrderItemAcceptedEvent(BaseEvent):
    order_item_id: int 

    def __post_init__(self):
        self.event_type = "OrderItemAccepted"


@dataclass
class OrderItemRejectedEvent(BaseEvent):
    order_item_id: int 

    def __post_init__(self):
        self.event_type = "OrderItemRejected"