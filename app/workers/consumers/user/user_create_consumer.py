from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class UserCreateConsumer(BaseConsumer):
    event_type = "UserCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        pass