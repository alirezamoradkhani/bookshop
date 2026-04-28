from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.order.models import enums
from app.exceptions.models.user import InvalidTokenUser,OnlyAdminPrimition
from app.exceptions.models.order_edition import OrderEditionNotFound


async def confirm_delivery_to_courier(uow: UnitOfWork,order_edition_id: int,token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role != Role.ADMIN:
            raise OnlyAdminPrimition
        order_edition = await uow.orderedition.get_by_order_edition_id(order_edition_id)
        if order_edition is None:
            raise OrderEditionNotFound
        await uow.orderedition.update_state(orderedition=order_edition,new_state=enums.OrderItemState.PREPARING) 
