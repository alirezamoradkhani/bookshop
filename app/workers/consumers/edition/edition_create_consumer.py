from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class EditionCreateConsumer(BaseConsumer):
    event_type = "EditionCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        pass