from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.borrow.models import model, enums
from app.user.models.model import User
from app.user.models.enums import UserPlan
from datetime import datetime

class Waitlistpository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self,waitlist:model.Waitlist):
        self.db.add(waitlist)
    
    async def get_by_edition_id(self,edition_id:int):
        result = await self.db.execute(select(model.Waitlist).where(model.Waitlist.edition_id == edition_id))
        return result.scalars().all()
    
    async def get_by_edition_id_and_user_plan(self,edition_id:int, user_plan:UserPlan):
        result = await self.db.execute(
            select(model.Waitlist)
            .join(User, User.id== model.Waitlist.user_id)
            .where(model.Waitlist.edition_id == edition_id,
            User.plan == user_plan))