from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.user.models import model, enums

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, id:int):
        new_user = model.User(id=id)
        self.db.add(new_user)
        return new_user
    async def get_by_id(self, id:int):
        result = await self.db.execute(select(model.User).where(model.User.id == id))
        return result.scalar_one_or_none()

    async def update_plan(self,new_plan: enums.UserPlan,id:int):
        result = await self.db.execute(select(model.User).where(model.User.id == id))
        user = result.scalar_one_or_none()
        user.plan = new_plan
        return user