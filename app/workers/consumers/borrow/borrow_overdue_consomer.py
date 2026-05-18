from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class BorrowOverdueConsumer(BaseConsumer):
    event_type = "BorrowOverdue"
    async def process(self, event: dict, uow:UnitOfWork):
        pass