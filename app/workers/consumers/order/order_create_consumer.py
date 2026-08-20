from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class OrderCreateConsumer(BaseConsumer):
    event_type = "OrderCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        order_id = event.get("order_id")
        if order_id is None or await uow.order.get_by_id(order_id) is None:
            raise ValueError(f"OrderCreated references missing order {order_id}")
