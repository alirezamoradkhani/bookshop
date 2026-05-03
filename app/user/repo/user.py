from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.user.models import model, enums
from datetime import datetime,timedelta

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

    async def update_plan(self,new_plan: enums.UserPlan,id:int,ex: datetime):
        result = await self.db.execute(select(model.User).where(model.User.id == id))
        user = result.scalar_one_or_none()
        user.plan = new_plan
        user.plan_expire = ex
        return user
    
    async def change_user_plan(self,user:model.User,new_plan:enums.UserPlan):
        user.plan = new_plan
        return user
    
    async def get_plan_by_id(self,user_id:int):
        result = await self.db.execute(select(model.User.plan).where(model.User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_plan_by_exp_date(self,now:datetime):
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        result = await self.db.execute(
            select(model.User)
            .where(model.User.plan_expire >= start
                   ,model.User.plan_expire < end
                   ,model.User.plan != enums.UserPlan.BRONZE)
                   )
        return result