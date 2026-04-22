from app.unit_of_work import UnitOfWork
from app.order.models import enums
from datetime import datetime, timedelta

async def mark_orderedition_as_forcereject(uow: UnitOfWork):
    now = datetime.utcnow()
    date = now - timedelta(days=6)
    async with uow:
        order_editions = await uow.orderedition.get_by_last_modify_and_state(state=enums.OrderItemState.PREPARING,date=date)
        for order_editioin in order_editions:
            await uow.orderedition.update_state(orderedition=order_editioin,new_state=enums.OrderItemState.FORCEREJECTED)