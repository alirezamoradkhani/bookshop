from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class OrderItemRejectConsumer(BaseConsumer):
    event_type = "OrderItemRejected"
    async def process(self, event: dict, uow:UnitOfWork):
        item_id = event.get("order_item_id")
        if item_id is None or await uow.orderedition.get_by_order_edition_id(item_id) is None:
            raise ValueError(f"OrderItemRejected references missing item {item_id}")
