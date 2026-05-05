from app.unit_of_work import UnitOfWork
from app.exceptions.models.user import InvalidOTP


async def delete_account(uow:UnitOfWork,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(token_data["user_id"])
        if current_user is None:
            raise InvalidOTP
        return await uow.baseusers.soft_delete(current_user)