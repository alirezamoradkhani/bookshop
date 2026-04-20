from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.user.models import model


class BaseUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(model.BaseUser).where(
                model.BaseUser.id == user_id,
                model.BaseUser.is_deleted == False
            )
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, user_name: str):
        result = await self.db.execute(
            select(model.BaseUser).where(
                model.BaseUser.username == user_name,
                model.BaseUser.is_deleted == False
            )
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, user_email: str):
        result = await self.db.execute(
            select(model.BaseUser).where(
                model.BaseUser.email == user_email,
                model.BaseUser.is_deleted == False
            )
        )
        return result.scalar_one_or_none()

    async def create(self, new_user: model.BaseUser):
        self.db.add(new_user)
        return new_user

    async def soft_delete(self, user: model.BaseUser):
        user.is_deleted = True
        return user