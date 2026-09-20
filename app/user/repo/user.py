from app.user.repo.baseuser import BaseUserRepository
from app.user.models.enums import UserPlan
from app.user.models.model import User
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class UserRepository(BaseUserRepository):
    async def create(self, id: int):
        return await self._insert(User(id=id))

    async def get_by_id(self, id: int):
        user = await super().get_by_id(id)
        return user if isinstance(user, User) else None

    async def update_plan(self, new_plan: UserPlan, id: int, ex: datetime):
        user = await self.get_by_id(id)
        if user is not None:
            user.plan, user.plan_expire = new_plan, ex
        return user

    async def change_user_plan(self, user: User, new_plan: UserPlan):
        user.plan = new_plan
        return user

    async def many_update_plan(self, user_ids: list[int], new_plan: UserPlan):
        await self.db.collection(self.collection).update_many(
            {"_id": {"$in": user_ids}}, {"$set": {"plan": serialize(new_plan)}}, **self.db.options()
        )

    async def get_plan_by_id(self, user_id: int):
        user = await self.get_by_id(user_id)
        return user.plan if user else None

    async def get_plan_by_exp_date(self, now: datetime):
        return await self._find({"plan_expire": {"$lt": now}, "plan": {"$ne": UserPlan.BRONZE.value}})
