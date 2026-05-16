from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app import models


async def test(db:AsyncSession):
    result = await db.execute(select(models.BaseUser))
    return result.scalars().all()

async def get_all_users(db: AsyncSession, token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if db_user.role != models.Role.ADMIN.value:
        raise HTTPException(status_code=400, detail="Only admin users can access this resource.")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.is_deleted == False))
    return result.scalars().all()
