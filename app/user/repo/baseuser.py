from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import case, select,update, func
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
    
    async def update_wallet_amount(self,user:model.BaseUser,new_amount:int):
        user.wallet_amount = new_amount
    
    async def increase_wallet_amount(self,user:model.BaseUser,change:int):
        user.wallet_amount += change

    async def many_increase_wallet(self, wallet_updates: list[tuple[int, int]]):

        stmt = (
            update(model.BaseUser)
            .where(model.BaseUser.id.in_([u[0] for u in wallet_updates]))
            .values(
                wallet_amount=model.BaseUser.wallet_amount + case(
                    {user_id: change for user_id, change in wallet_updates},
                    value=model.BaseUser.id
                )
            )
        )

        await self.db.execute(stmt)

    async def decrease_wallet_amount(self,user:model.BaseUser,change:int):
        user.wallet_amount -= change

    async def get_by_username(self,name:str):
        result = await self.db.execute(select(model.BaseUser).where(model.BaseUser.username == name))
        return result.scalar_one_or_none()