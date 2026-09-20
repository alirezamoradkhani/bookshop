from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from typing import Any

from pymongo import ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase

from app.mongo.serialization import serialize


class MongoRepository:
    collection: str
    model: type
    enum_fields: dict[str, type[Enum]] = {}

    def __init__(self, database: AsyncDatabase, session_provider: Callable[[], Any]):
        self.database = database
        self._session_provider = session_provider

    def _collection(self, name: str | None = None):
        return self.database[name or self.collection]

    def _options(self) -> dict[str, Any]:
        session = self._session_provider()
        return {"session": session} if session is not None else {}

    async def _next_id(self) -> int:
        result = await self._collection("counters").find_one_and_update(
            {"_id": self.collection},
            {"$inc": {"value": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
            **self._options(),
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
        return self.model(**payload)

    async def _insert(self, obj: Any):
        object_id = getattr(obj, "id", None)
        if object_id is None:
            object_id = await self._next_id()
            if hasattr(obj, "order_edition_id"):
                obj.order_edition_id = object_id
            else:
                obj.id = object_id
        document = {"_id": object_id, **serialize(obj)}
        await self._collection().insert_one(document, **self._options())
        return obj

    async def _find_one(self, query: dict[str, Any]):
        document = await self._collection().find_one(query, **self._options())
        return self._make(document)

    async def _find(self, query: dict[str, Any] | None = None, sort: tuple[str, int] | None = None):
        cursor = self._collection().find(query or {}, **self._options())
        if sort:
            cursor = cursor.sort(*sort)
        return [self._make(document) async for document in cursor]

    async def _set_fields(self, obj: Any, **changes: Any):
        await self._collection().update_one(
            {"_id": obj.id},
            {"$set": serialize(changes)},
            **self._options(),
        )
        for field, value in changes.items():
            setattr(obj, field, value)
        return obj

    async def _increment_fields(self, obj: Any, **changes: int):
        await self._collection().update_one(
            {"_id": obj.id},
            {"$inc": changes},
            **self._options(),
        )
        for field, change in changes.items():
            setattr(obj, field, getattr(obj, field) + change)
        return obj

    async def _delete(self, obj: Any):
        await self._collection().delete_one({"_id": obj.id}, **self._options())
