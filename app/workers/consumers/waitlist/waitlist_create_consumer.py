from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class WaitlistCreate(BaseConsumer):
    event_type = "WaitlistCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        pass