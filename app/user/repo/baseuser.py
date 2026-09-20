from app.mongo.base import MongoRepository
from app.user.models.enums import Role, UserPlan
from app.user.models.model import Admin, Author, BaseUser, User
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class BaseUserRepository(MongoRepository):
    collection, model = "users", BaseUser

    def _make(self, data):
        if data is None:
            return None
        payload = dict(data)
        payload.pop("_id", None)
        role = payload.get("role", Role.USER.value)
        role = role if isinstance(role, Role) else Role(role)
        payload["role"] = role
        cls = {Role.USER: User, Role.AUTHOR: Author, Role.ADMIN: Admin}.get(role, BaseUser)
        if cls is User:
            plan = payload.get("plan", UserPlan.BRONZE)
            payload["plan"] = plan if isinstance(plan, UserPlan) else UserPlan(plan)
        return cls(**payload)

    async def get_by_id(self, user_id: int):
        return await self._find_one({"_id": user_id, "is_deleted": False})

    async def get_by_ids(self, user_ids: list[int]):
        return await self._find({"_id": {"$in": user_ids}, "is_deleted": False})

    async def get_by_username(self, user_name: str):
        return await self._find_one({"username": user_name, "is_deleted": False})

    async def get_by_email(self, user_email: str):
        return await self._find_one({"email": user_email, "is_deleted": False})

    async def create(self, new_user: BaseUser):
        return await self._insert(new_user)

    async def soft_delete(self, user: BaseUser):
        return await self._set_fields(user, is_deleted=True)

    async def update_wallet_amount(self, user: BaseUser, new_amount: int):
        return await self._set_fields(user, wallet_amount=new_amount)

    async def increase_wallet_amount(self, user: BaseUser, change: int):
        return await self._increment_fields(user, wallet_amount=change)

    async def many_increase_wallet(self, wallet_updates: list[tuple[int, int]]):
        for user_id, change in wallet_updates:
            await self._collection().update_one(
                {"_id": user_id}, {"$inc": {"wallet_amount": change}}, **self._options()
            )

    async def decrease_wallet_amount(self, user: BaseUser, change: int):
        return await self._increment_fields(user, wallet_amount=-change)
