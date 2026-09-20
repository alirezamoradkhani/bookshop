from app.mongo.base import MongoRepository
from app.outbox.model import OutboxEvent
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class OutboxRepository(MongoRepository):
    collection, model = "outbox_events", OutboxEvent

    async def add(self, event: OutboxEvent):
        if event.created_at is None:
            event.created_at = datetime.utcnow()
        return await self._insert(event)

    async def get_unprocessed(self, limit: int):
        return (await self._find({"processed": False}, ("id", 1)))[:limit]

    async def mark_processed(self, event: OutboxEvent):
        return await self._set_fields(event, processed=True)
