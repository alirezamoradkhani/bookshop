from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.outbox.model import OutboxEvent

class OutboxRepository:

    def __init__(self, db:AsyncSession):
        self.db = db

    async def add(self, event: OutboxEvent):
        self.db.add(event)

    async def get_unprocessed(self,limit:int):
        query = (
            select(OutboxEvent)
            .where(OutboxEvent.processed == False)
            .order_by(OutboxEvent.id)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
