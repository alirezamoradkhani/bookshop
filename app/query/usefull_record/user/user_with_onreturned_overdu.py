from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select,func,desc
from app.models import *


async def user_with_over_due(db: AsyncSession):
    result = await db.execute(
        select(BaseUser.id,
               BaseUser.username,
               Borrow.id,
               Borrow.borrowed_at,
               Borrow.due_at)
               .join(Borrow,Borrow.user_id == BaseUser.id)
               .where(Borrow.is_overdue == True
                      ,Borrow.status == BorrowStatus.ACTIVE)
    )
    return result.all()