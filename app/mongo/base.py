from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from pymongo import ReturnDocument

from app.mongo.database import MongoContext
from app.mongo.serialization import serialize

class MongoRepository:
    collection: str
    model: type
    enum_fields: dict[str, type[Enum]] = {}

    def __init__(self, db: MongoContext):
        self.db = db

    async def _next_id(self) -> int:
        result = await self.db.collection("counters").find_one_and_update(
            {"_id": self.collection},
            {"$inc": {"value": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
            **self.db.options(),
        )
        return int(result["value"])

    def _make(self, data: dict[str, Any] | None):
        if data is None:
            return None
        payload = dict(data)
        payload.pop("_id", None)
        for field, enum_type in self.enum_fields.items():
            value = payload.get(field)
            if value is not None and not isinstance(value, enum_type):
                payload[field] = enum_type(value)
        return self.db.track(self.model(**payload), self.collection)

    async def _insert(self, obj: Any):
        object_id = getattr(obj, "id", None)
        if object_id is None:
            object_id = await self._next_id()
            if hasattr(obj, "order_edition_id"):
                obj.order_edition_id = object_id
            else:
                obj.id = object_id
        document = {"_id": object_id, **serialize(obj)}
        await self.db.collection(self.collection).insert_one(document, **self.db.options())
        self.db.track(obj, self.collection)
        return obj

    async def _find_one(self, query: dict[str, Any]):
        document = await self.db.collection(self.collection).find_one(query, **self.db.options())
        return self._make(document)

    async def _find(self, query: dict[str, Any] | None = None, sort: tuple[str, int] | None = None):
        cursor = self.db.collection(self.collection).find(query or {}, **self.db.options())
        if sort:
            cursor = cursor.sort(*sort)
        return [self._make(document) async for document in cursor]

    async def _replace(self, obj: Any):
        await self.db.collection(self.collection).replace_one(
            {"_id": obj.id}, {"_id": obj.id, **serialize(obj)}, upsert=True, **self.db.options()
        )

    async def _delete(self, obj: Any):
        await self.db.collection(self.collection).delete_one({"_id": obj.id}, **self.db.options())
