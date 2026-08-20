from app.core.unit_of_work import UnitOfWork
from app.order.models import enums
from datetime import datetime, timedelta
from app.events.order.order_events import OrderItemRejectedEvent
from app.events.base import event_to_payload
from app.outbox.model import OutboxEvent

async def mark_orderedition_as_forcereject(uow_factory):
    now = datetime.utcnow()
    date = now - timedelta(days=6)
    async with uow_factory() as uow:
        order_editions = await uow.orderedition.get_by_last_modify_and_state(state=enums.OrderItemState.PREPARING,date=date)
        for order_edition in order_editions:
            order = await uow.order.get_by_id(order_edition.order_id)
            edition = await uow.edition.get_by_id(order_edition.edition_id)
            if order is None or edition is None:
                continue
            customer = await uow.baseusers.get_by_id(order.user_id)
            if customer is None:
                continue
            await uow.orderedition.update_state(
                orderedition=order_edition,
                new_state=enums.OrderItemState.FORCEREJECTED,
            )
            await uow.order.update_final_price(order=order, change=order_edition.price)
            await uow.baseusers.increase_wallet_amount(user=customer, change=order_edition.price)
            await uow.edition.update_amount(edition=edition, new_amount=edition.amount + 1)
            event = OrderItemRejectedEvent(order_item_id=order_edition.order_edition_id)
            await uow.outbox.add(OutboxEvent(
                event_type=event.event_type,
                payload=event_to_payload(event),
            ))
