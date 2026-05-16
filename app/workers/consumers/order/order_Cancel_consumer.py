from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class OrderCancelConsumer(BaseConsumer):
    event_type = "OrderCanceled"
    async def process(self, event: dict, uow:UnitOfWork):
        pass