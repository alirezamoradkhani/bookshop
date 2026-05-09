from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class EditionUpdateConsumer(BaseConsumer):
    event_type = "EditionUpdated"
    async def process(self, event: dict, uow:UnitOfWork):
        pass