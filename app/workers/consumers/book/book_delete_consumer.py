from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class BookDeleteConsumer(BaseConsumer):
    event_type = "BookDeleted"
    async def process(self, event: dict, uow:UnitOfWork):
        pass