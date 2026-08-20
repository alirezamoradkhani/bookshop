from app.transaction.schemas.outputs import BaseUserResponse
from app.core.unit_of_work import UnitOfWork
from app.transaction.models.model import Transaction
from app.transaction.models.enums import TransactionType
from datetime import datetime
from app.exceptions.models.user import InvalidTokenUser
from app.exceptions.models.transaction import ReciverNotFound, InsufficientFunds
from app.exceptions.models.edition import InvalidAmount


async def transfer(uow:UnitOfWork,amount:int,token_data: dict,reciver_id :int):
    if amount <= 0:
        raise InvalidAmount
    async with uow:
        user_ids = sorted({token_data["user_id"], reciver_id})
        users = await uow.baseusers.get_by_ids(user_ids, for_update=True)
        users_by_id = {user.id: user for user in users}
        current_user = users_by_id.get(token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        reciver = users_by_id.get(reciver_id)
        if reciver is None:
            raise ReciverNotFound
        if current_user.id == reciver.id or current_user.wallet_amount < amount:
            raise InsufficientFunds
        send_transaction = Transaction(user_id=current_user.id,amount=amount,date=datetime.utcnow(),type=TransactionType.SEND)
        await uow.transaction.create(send_transaction)
        await uow.flush()
        recive_transaction = Transaction(user_id=reciver.id,amount=amount,date=datetime.utcnow(),type=TransactionType.RECEIVE)
        await uow.transaction.create(recive_transaction)

        await uow.baseusers.decrease_wallet_amount(user=current_user,change=amount)
        await uow.baseusers.increase_wallet_amount(user=reciver,change=amount)

        return BaseUserResponse.model_validate(current_user).model_dump()
