from app.core.unit_of_work import UnitOfWork
from app.events.borrow.borrow_events import BorrowOverdueEvent
from app.events.base import event_to_payload
from app.outbox.model import OutboxEvent
from datetime import datetime

async def mark_borrow_as_overdue(uow_factory):
    async with uow_factory() as uow:
        now = datetime.utcnow()
        borrows = await uow.borrow.get_owerdue_by_date(now=now)
        await uow.borrow.mark_many_as_overdue(borrows=borrows)
        for borrow in borrows:
            event = BorrowOverdueEvent(borrow_id=borrow.id, user_id=borrow.user_id)
            await uow.outbox.add(OutboxEvent(
                event_type=event.event_type,
                payload=event_to_payload(event),
            ))
