from app.core.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyUserHavePrimition
from app.exceptions.models.order import OrderNotFound
from app.order.schemas.outputs import OrderDetailsResponse


async def get_user_orders(uow:UnitOfWork,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        return await uow.order.get_by_user_id(id=current_user.id)

async def get_order_details(uow: UnitOfWork, token_data: dict, order_id: int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id=token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        order = await uow.order.get_by_id(order_id)
        if order is None or order.user_id != current_user.id:
            raise OrderNotFound
        items = await uow.orderedition.get_by_order_id(order.id)
        return OrderDetailsResponse(
            id=order.id,
            user_id=order.user_id,
            state=order.state,
            final_price=order.final_price,
            date=order.date,
            items=items,
        )
