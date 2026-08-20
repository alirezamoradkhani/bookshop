from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class WaitlistCreateConsumer(BaseConsumer):
    event_type = "WaitlistCreated"
    async def process(self, event: dict, uow:UnitOfWork):
        user_id = event.get("user_id")
        edition_id = event.get("edition_id")
        if user_id is None or edition_id is None:
            raise ValueError("WaitlistCreated event is missing identifiers")
        if await uow.baseusers.get_by_id(user_id) is None:
            raise ValueError(f"WaitlistCreated references missing user {user_id}")
        if await uow.edition.get_by_id(edition_id) is None:
            raise ValueError(f"WaitlistCreated references missing edition {edition_id}")
