from __future__ import annotations

from typing import Any

from pymongo import AsyncMongoClient

from app.core.setting import settings
from app.mongo.serialization import serialize


class MongoContext:
    """Request/use-case database context compatible with the old UnitOfWork API.

    Mongo writes are immediate by default. Set MONGO_TRANSACTIONS=true and use a
    replica set when a deployment requires multi-collection transactions.
    """

    def __init__(self, database: Any, client: AsyncMongoClient):
        self.database = database
        self.client = client
        self.session = None
        self._tracked: dict[tuple[str, int], Any] = {}
        self._transaction_enabled = settings.mongo_transactions

    def collection(self, name: str):
        return self.database[name]

    def track(self, obj: Any, collection: str):
        object_id = getattr(obj, "id", None)
        if object_id is not None:
            self._tracked[(collection, object_id)] = obj
        return obj

    async def __aenter__(self):
        if self._transaction_enabled:
            self.session = await self.client.start_session()
            self.session.start_transaction()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.flush()
            await self.commit()
        if self.session is not None:
            await self.session.end_session()
            self.session = None

    def options(self) -> dict[str, Any]:
        return {"session": self.session} if self.session is not None else {}

    async def flush(self):
        for (collection, object_id), obj in list(self._tracked.items()):
            await self.collection(collection).replace_one(
                {"_id": object_id},
                {"_id": object_id, **serialize(obj)},
                upsert=True,
                **self.options(),
            )

    async def commit(self):
        if self.session is not None and self.session.in_transaction:
            await self.session.commit_transaction()

    async def rollback(self):
        if self.session is not None and self.session.in_transaction:
            await self.session.abort_transaction()
        self._tracked.clear()
