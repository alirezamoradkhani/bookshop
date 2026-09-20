from app.user.repo.baseuser import BaseUserRepository
from app.user.models.enums import Role
from app.user.models.model import Author
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class AuthorRepository(BaseUserRepository):
    async def create(self, id: int):
        return await self._insert(Author(id=id))

    async def get_by_id(self, id: int):
        user = await super().get_by_id(id)
        return user if isinstance(user, Author) else None

    async def get_by_name(self, name: str):
        user = await self._find_one({"username": name, "role": Role.AUTHOR.value})
        return user

    async def get_by_names(self, names: list[str]):
        return await self._find({"username": {"$in": names}, "role": Role.AUTHOR.value})

    async def get_by_ids(self, ids: list[int]):
        return await self._find({"_id": {"$in": ids}, "role": Role.AUTHOR.value})

    async def search(self, id=None, name=None):
        query: dict[str, Any] = {"role": Role.AUTHOR.value}
        if id:
            query["_id"] = id
        if name:
            query["username"] = {"$regex": name, "$options": "i"}
        return await self._find(query)
