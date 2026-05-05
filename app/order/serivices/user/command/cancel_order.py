from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.order.models import enums
from app.exceptions.models.user import InvalidTokenUser,OnlyUserHavePrimition,UserPermissionDenied
from app.exceptions.models.order import OrderNotCancelable,OrderNotFound


async def cancel_order(uow:UnitOfWork,order_id: int, token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        order = await uow.order.get_by_id(order_id)
        if order is None:
                raise OrderNotFound

        if current_user.role == Role.AUTHOR:
             raise OnlyUserHavePrimition
        await uow.flush()
        order_editions = await uow.orderedition.get_by_order_id(order.id)
        if current_user.role == Role.USER:
            if order.user_id != current_user.id:
                raise UserPermissionDenied
            for order_edition in order_editions:
                if order_edition.state not in [enums.OrderItemState.WAITING,enums.OrderItemState.REJECTED,enums.OrderItemState.CANCELED]:
                    raise OrderNotCancelable
            await uow.order.update_order_atate(order=order,new_state=enums.OrderState.CANCELED)
            for order_edition in order_editions:
                await uow.orderedition.update_state(orderedition=order_edition,new_state=enums.OrderItemState.CANCELED)
            await uow.baseusers.increase_wallet_amount(user=current_user,change=order.final_price)
                
        return order