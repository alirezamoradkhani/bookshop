from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class OrderItemRejectConsumer(BaseConsumer):
    event_type = "OrderItemRejected"
    async def process(self, event: dict, uow:UnitOfWork):
        pass