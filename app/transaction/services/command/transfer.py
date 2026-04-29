from app.unit_of_work import UnitOfWork
from app.transaction.models.model import Transaction
from app.transaction.models.enums import TransactionType
from datetime import datetime
from app.exceptions.models.user import InvalidTokenUser
from app.exceptions.models.transaction import ReciverNotFound, InsufficientFunds


async def transfer(uow:UnitOfWork,amount:int,token_data: dict,reciver_id :int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        reciver = await uow.baseusers.get_by_id(user_id= reciver_id)
        if reciver is None:
            raise ReciverNotFound
        if current_user.wallet_amount <= amount:
            raise InsufficientFunds
        send_transaction = Transaction(user_id=current_user.id,amount=amount,date=datetime.utcnow(),type=TransactionType.SEND)
        await uow.transaction.create(send_transaction)
        await uow.flush()
        recive_transaction = Transaction(user_id=reciver.id,amount=amount,date=datetime.utcnow(),type=TransactionType.RECEIVE)
        await uow.transaction.create(recive_transaction)

        await uow.baseusers.decrease_wallet_amount(user=current_user,change=amount)
        await uow.baseusers.increase_wallet_amount(user=reciver,change=amount)

        return current_user