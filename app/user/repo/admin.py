from app.user.repo.baseuser import BaseUserRepository
from app.user.models.model import Admin
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class AdminRepository(BaseUserRepository):
    async def create(self, id: int):
        return await self._insert(Admin(id=id))
