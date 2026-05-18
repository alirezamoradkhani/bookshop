from app.core.unit_of_work import UnitOfWork
from app.order.models import enums
from datetime import datetime, timedelta

async def mark_orderedition_as_forcereject(uow_factory):
    now = datetime.utcnow()
    date = now - timedelta(days=6)
    async with uow_factory() as uow:
        order_editions = await uow.orderedition.get_by_last_modify_and_state(state=enums.OrderItemState.PREPARING,date=date)
        await uow.orderedition.many_update_state(
            order_edition_ids=[oe.order_edition_id for oe in order_editions],
            new_state=enums.OrderItemState.FORCEREJECTED
        )