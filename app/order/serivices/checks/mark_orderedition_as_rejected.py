from app.unit_of_work import UnitOfWork
from app.order.models import enums
from datetime import datetime, timedelta

async def mark_orderedition_as_rejected(uow: UnitOfWork):
    now = datetime.utcnow()
    date = now - timedelta(days=2)
    async with uow:
        order_editions = await uow.orderedition.get_by_last_modify_and_state(state=enums.OrderItemState.WAITING,date=date)
        await uow.orderedition.many_update_state(
            order_edition_ids=[oe.order_edition_id for oe in order_editions],
            new_state=enums.OrderItemState.REJECTED
        )