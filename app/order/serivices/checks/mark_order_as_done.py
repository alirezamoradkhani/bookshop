from app.unit_of_work import UnitOfWork
from app.order.models import enums, model


async def mark_ordere_as_done(uow_factory):
    async with uow_factory() as uow:
        orders = await uow.order.get_by_state(enums.OrderState.IN_PROCCESE)

        if not orders:
            return

        order_ids = [o.id for o in orders]

        order_editions = await uow.orderedition.get_by_order_ids(order_ids)

        grouped: dict = {}
        for oe in order_editions:
            grouped.setdefault(oe.order_id, []).append(oe)

        to_update = []

        for order in orders:
            items = grouped.get(order.id, [])

            if all(
                item.state not in [
                    enums.OrderItemState.ACCEPTED,
                    enums.OrderItemState.PREPARING,
                    enums.OrderItemState.WAITING
                ]
                for item in items
            ):
                to_update.append(order)

        await uow.order.many_update_state(
            order_ids=order_ids,
            new_state=enums.OrderState.DONE
        )