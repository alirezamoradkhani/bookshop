from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.outbox.model import OutboxEvent

class OutboxRepository:

    def __init__(self, db:AsyncSession):
        self.db = db

    async def add(self, event: OutboxEvent):
        self.db.add(event)

    async def get_unprocessed(self):
        result = await self.db.execute(
            select(OutboxEvent).where(OutboxEvent.processed == False)
        )
        return result.scalars().all()