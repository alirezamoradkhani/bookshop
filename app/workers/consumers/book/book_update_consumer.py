from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class BookUpdateConsumer(BaseConsumer):
    event_type = "BookUpdated"
    async def process(self, event: dict, uow:UnitOfWork):
        pass