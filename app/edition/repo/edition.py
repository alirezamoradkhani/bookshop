from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.edition.models.model import Edition


class EditionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_edition(self,new_edition: Edition):
        self.db.add(new_edition)
    
    async def get_edition(self,edition_id:int):
        result = await self.db.execute(select(Edition).where(Edition.id == edition_id))

    async def update_amount(self,edition:Edition ,new_amount:int):
        edition.amount = new_amount

    async def update_price(self,edition:Edition ,new_price:int):
        edition.price = new_price

    async def soft_delete(self,edition:Edition):
        edition.is_deleted = True