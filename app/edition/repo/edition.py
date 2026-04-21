from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.edition.models.model import Edition


class EditionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_edition(self,new_edition: Edition):
        self.db.add(new_edition)
    
    async def get_by_id(self,edition_id:int):
        result = await self.db.execute(select(Edition).where(Edition.id == edition_id, Edition.is_deleted == False))
        return result.scalar_one_or_none()

    async def update_amount(self,edition:Edition ,new_amount:int):
        edition.amount = new_amount

    async def update_price(self,edition:Edition ,new_price:int):
        edition.price = new_price

    async def soft_delete(self,edition:Edition):
        edition.is_deleted = True