from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.borrow.models import model, enums
from datetime import datetime

class Borrowpository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self,new_borrow:model.Borrow):
        self.db.add(new_borrow)

    async def get_by_id(self,borrow_id:int):
        result = await self.db.execute(select(model.Borrow).where(model.Borrow.id == borrow_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int):
        result = await self.db.execute(
            select(model.Borrow)
            .where(model.Borrow.user_id == user_id)
            .order_by(model.Borrow.borrowed_at.desc())
        )
        return result.scalars().all()

    async def get_active_by_user_and_edition(self, user_id: int, edition_id: int):
        result = await self.db.execute(
            select(model.Borrow).where(
                model.Borrow.user_id == user_id,
                model.Borrow.edition_id == edition_id,
                model.Borrow.status == enums.BorrowStatus.ACTIVE,
            )
        )
        return result.scalar_one_or_none()

    async def update_status(self,borrow:model.Borrow,new_status:enums.BorrowStatus):
        borrow.status = new_status

    async def set_Return_time(self,borrow:model.Borrow,return_time:datetime):
        borrow.returned_at = return_time

    async def get_owerdue_by_date(self,now:datetime):
        result = await self.db.execute(
            select(model.Borrow)
            .where(model.Borrow.due_at < now,
                   model.Borrow.status == enums.BorrowStatus.ACTIVE,
                   model.Borrow.is_overdue == False)
                   )
        return result.scalars().all()
    
    async def mark_as_owerdue(self,borrow:model.Borrow):
        borrow.is_overdue = True

    async def mark_many_as_overdue(self, borrows: list[model.Borrow]):
        borrow_ids = [borrow.id for borrow in borrows]
        await self.db.execute(
            update(model.Borrow)
            .where(model.Borrow.id.in_(borrow_ids))
            .values(is_overdue=True)
        )
