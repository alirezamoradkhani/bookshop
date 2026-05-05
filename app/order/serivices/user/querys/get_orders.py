from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyUserHavePrimition


async def get_user_orders(uow:UnitOfWork,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        return await uow.order.get_by_user_id(id=current_user.id)
