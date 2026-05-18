from app.core.unit_of_work import UnitOfWork
from app.order.models import enums


async def mark_ordere_as_inprogres(uow_factory):
    async with uow_factory() as uow:
        orders = await uow.order.get_by_state(enums.OrderState.WAITING)

        if not orders:
            return

        order_ids = [o.id for o in orders]

        order_editions = await uow.orderedition.get_by_order_ids(order_ids)

        grouped: dict = {}
        for oe in order_editions:
            grouped.setdefault(oe.order_id, []).append(oe)

        to_update = []

        active_states = {
            enums.OrderItemState.ACCEPTED,
            enums.OrderItemState.PREPARING
        }

        for order in orders:
            items = grouped.get(order.id, [])

            if any(item.state in active_states for item in items):
                to_update.append(order.id)

        if not to_update:
            return

        await uow.order.many_update_state(
            order_ids=to_update,
            new_state=enums.OrderState.IN_PROCCESE
        )