from fastapi import HTTPException
from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.order.models import enums


async def confirm_delivery_to_courier(uow: UnitOfWork,order_edition_id: int,token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        if current_user.role != Role.ADMIN:
            raise HTTPException(status_code=400, detail="only admin have permission.")
        order_edition = await uow.orderedition.get_by_order_edition_id(order_edition_id)
        if order_edition is None:
            raise HTTPException(status_code=400, detail="orderedition not found.")
        await uow.orderedition.update_state(orderedition=order_edition,new_state=enums.OrderItemState.PREPARING) 
