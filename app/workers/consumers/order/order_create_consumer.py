from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class OrderCreateConsumer(BaseConsumer):
    event_type = "OrderCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        pass