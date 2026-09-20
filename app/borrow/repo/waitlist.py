from app.mongo.base import MongoRepository
from app.borrow.models.model import Waitlist
from app.user.models.enums import UserPlan
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class Waitlistpository(MongoRepository):
    collection, model = "waitlist", Waitlist

    async def create(self, waitlist: Waitlist):
        return await self._insert(waitlist)

    async def get_by_edition_id(self, edition_id: int):
        return await self._find({"edition_id": edition_id}, ("created_at", 1))

    async def get_by_edition_id_and_user_plan(self, edition_id: int, user_plan: UserPlan):
        for item in await self.get_by_edition_id(edition_id):
            user = await self.db.collection("users").find_one({"_id": item.user_id, "plan": serialize(user_plan)}, **self.db.options())
            if user:
                return item
        return None

    async def get_by_user_id_and_edition_id(self, edition_id: int, user_id: int):
        return await self._find_one({"edition_id": edition_id, "user_id": user_id})

    async def delete(self, waitlist: Waitlist):
        await self._delete(waitlist)
