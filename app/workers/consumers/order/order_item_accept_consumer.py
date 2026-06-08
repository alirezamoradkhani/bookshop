from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class OrderItemAcceptConsumer(BaseConsumer):
    event_type = "OrderItemAccepted"
    async def process(self, event: dict, uow:UnitOfWork):
        pass