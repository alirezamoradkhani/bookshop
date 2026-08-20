from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class UserCreateConsumer(BaseConsumer):
    event_type = "UserCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        user_id = event.get("user_id")
        if user_id is None or await uow.baseusers.get_by_id(user_id) is None:
            raise ValueError(f"UserCreated references missing user {user_id}")
