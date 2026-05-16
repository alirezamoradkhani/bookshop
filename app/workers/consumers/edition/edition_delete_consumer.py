from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class EditionDeleteConsumer(BaseConsumer):
    event_type = "EditionDeleted"
    async def process(self, event: dict, uow:UnitOfWork):
        pass