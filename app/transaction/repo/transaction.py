from app.mongo.base import MongoRepository
from app.transaction.models.enums import TransactionType
from app.transaction.models.model import Transaction
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class TransactionRepository(MongoRepository):
    collection, model = "transactions", Transaction
    enum_fields = {"type": __import__("app.transaction.models.enums", fromlist=["TransactionType"]).TransactionType}

    async def create(self, transaction: Transaction):
        return await self._insert(transaction)

    async def get_by_user_id(self, user_id: int):
        return await self._find({"user_id": user_id}, ("date", -1))
