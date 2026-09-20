from app.mongo.base import MongoRepository
from app.borrow.models.enums import BorrowStatus
from app.borrow.models.model import Borrow
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class Borrowpository(MongoRepository):
    collection, model = "borrows", Borrow
    enum_fields = {"status": BorrowStatus}

    async def create(self, new_borrow: Borrow):
        return await self._insert(new_borrow)

    async def get_by_id(self, borrow_id: int, for_update: bool = False):
        return await self._find_one({"_id": borrow_id})

    async def get_by_user_id(self, user_id: int):
        return await self._find({"user_id": user_id}, ("borrowed_at", -1))

    async def get_active_by_user_and_edition(self, user_id: int, edition_id: int):
        return await self._find_one({"user_id": user_id, "edition_id": edition_id, "status": BorrowStatus.ACTIVE.value})

    async def update_status(self, borrow: Borrow, new_status: BorrowStatus):
        borrow.status = new_status

    async def set_Return_time(self, borrow: Borrow, return_time: datetime):
        borrow.returned_at = return_time

    async def get_owerdue_by_date(self, now: datetime):
        return await self._find({"due_at": {"$lt": now}, "status": BorrowStatus.ACTIVE.value, "is_overdue": False})

    async def mark_as_owerdue(self, borrow: Borrow):
        borrow.is_overdue = True

    async def mark_many_as_overdue(self, borrows: list[Borrow]):
        await self.db.collection(self.collection).update_many(
            {"_id": {"$in": [borrow.id for borrow in borrows]}}, {"$set": {"is_overdue": True}}, **self.db.options()
        )
