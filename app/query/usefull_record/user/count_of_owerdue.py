from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select,func,desc
from app.models import *


async def count_of_owerdue(db:AsyncSession,user:BaseUser):
    result = await db.execute(
        select(func.count(Borrow.id).label("count_od_overdue"))
        .join(BaseUser,BaseUser.id == Borrow.user_id)
        .where(
            BaseUser.id == user.id
            ,Borrow.is_overdue == True
        )
    )
    return result.scalar_one_or_none()