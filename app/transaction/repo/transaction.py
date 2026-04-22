from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.transaction.models import model
from app.order.models import enums


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self,transaction:model.Transaction):
        self.db.add(transaction)
    
    async def get_by_user_id(self,user_id:int):
        result = await self.db.execute(select(model.Transaction).where(model.Transaction.user_id == user_id))
        return result.scalars().all()