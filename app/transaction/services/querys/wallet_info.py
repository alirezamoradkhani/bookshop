from app.unit_of_work import UnitOfWork
from app.transaction.models.model import Transaction
from app.transaction.models.enums import TransactionType
from datetime import datetime
from app.exceptions.models.user import InvalidTokenUser


async def walletinfo(uow:UnitOfWork,token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        transactions = await uow.transaction.get_by_user_id(user_id=current_user.id)
        response_trransaction = []
        for t in transactions:
            response_trransaction.append(
                {"id" : t.id
                 ,"type" : t.type
                 ,"amount" : t.amount
                 ,"date" : t.date})
        return {"walet_amount" : current_user.wallet_amount,
                "transactions" : response_trransaction
                }