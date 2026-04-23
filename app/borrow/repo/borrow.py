from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.borrow.models import model, enums
from datetime import datetime,timedelta

class Borrowpository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self,new_borrow:model.Borrow):
        self.db.add(new_borrow)

    async def get_by_id(self,borrow_id:int):
        result = await self.db.execute(select(model.Borrow).where(model.Borrow.id == borrow_id))
        return result.scalar_one_or_none()

    async def update_status(self,borrow:model.Borrow,new_status:enums.BorrowStatus):
        borrow.status = new_status

    async def set_Return_time(self,borrow:model.Borrow,return_time:datetime):
        borrow.returned_at = return_time

    async def get_owerdue_by_date(self,now:datetime):
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        result = await self.db.execute(
            select(model.Borrow)
            .where(model.Borrow.due_at >= start
                   ,model.Borrow.due_at < end
                   ,model.Borrow.status == enums.BorrowStatus.ACTIVE)
                   )
        return result.scalars().all()
    
    async def mark_as_owerdue(self,borrow:model.Borrow):
        borrow.is_overdue = True
