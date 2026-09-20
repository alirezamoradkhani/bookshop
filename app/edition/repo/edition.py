from app.mongo.base import MongoRepository
from app.edition.models.model import Edition
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class EditionRepository(MongoRepository):
    collection, model = "editions", Edition

    async def create_edition(self, new_edition: Edition):
        return await self._insert(new_edition)

    async def get_by_id(self, edition_id: int, for_update: bool = False):
        return await self._find_one({"_id": edition_id, "is_deleted": False})

    async def get_by_ids(self, edition_ids: list[int], for_update: bool = False):
        return await self._find({"_id": {"$in": edition_ids}, "is_deleted": False})

    async def update_amount(self, edition: Edition, new_amount: int):
        edition.amount = new_amount

    async def update_price(self, edition: Edition, new_price: int):
        edition.price = new_price

    async def soft_delete(self, edition: Edition):
        edition.is_deleted = True

    async def get_by_book_id(self, book_id: int):
        return await self._find({"book_id": book_id})

    async def get_by_book_ids(self, book_ids: list[int]):
        return await self._find({"book_id": {"$in": book_ids}})
