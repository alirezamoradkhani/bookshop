from app.unit_of_work import UnitOfWork
from app.order.models import enums
from datetime import datetime, timedelta

async def mark_ordere_as_inprogres(uow: UnitOfWork):
    async with uow:
        orders = await uow.order.get_by_state(enums.OrderState.IN_PROCCESE)
        for order in orders:
            order_editions = await uow.orderedition.get_by_order_id(order.id)
            for order_edition in order_editions:
                if order_edition.state in [enums.OrderItemState.ACCEPTED,enums.OrderItemState.PREPARING,enums.OrderItemState.WAITING] :
                    break
                else:
                    await uow.order.update_order_atate(order=order,new_state=enums.OrderState.DONE)

        