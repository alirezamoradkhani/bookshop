from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.transaction.models import model
from app.order.models import enums


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self,transaction:model.Transaction):
        self.db.add(transaction)