from app.unit_of_work import UnitOfWork
from app.transaction.models.model import Transaction
from app.transaction.models.enums import TransactionType
from datetime import datetime
from app.exceptions.models.user import InvalidTokenUser
from app.exceptions.models.transaction import InsufficientFunds

async def withdraw(uow:UnitOfWork,amount:int,token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.wallet_amount <= amount:
            raise InsufficientFunds
        new_transaction = Transaction(user_id=current_user.id,amount=amount,date=datetime.utcnow(),type=TransactionType.WITHDRAWAL)
        await uow.transaction.create(new_transaction)
        await uow.baseusers.decrease_wallet_amount(user= current_user,change=amount)
        return current_user