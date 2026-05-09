from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class BorrowCreatedConsumer(BaseConsumer):
    event_type = "BorrowCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        pass