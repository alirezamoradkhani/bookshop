from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import *


async def user_with_over_due(db: AsyncSession):
    result = await db.execute(
        select(BaseUser.id.label("user_id"),
               BaseUser.username.label("user_name"),
               Borrow.id.label("borrow_id"),
               Borrow.borrowed_at.label("borrow_start"),
               Borrow.due_at.label("borrow_end"))
               .join(Borrow,Borrow.user_id == BaseUser.id)
               .where(Borrow.is_overdue == True
                      ,Borrow.status == BorrowStatus.ACTIVE)
    )
    return result.all()