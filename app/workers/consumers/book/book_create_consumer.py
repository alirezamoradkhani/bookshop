from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class BookCreateConsumer(BaseConsumer):
    
    event_type = "BookCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        pass