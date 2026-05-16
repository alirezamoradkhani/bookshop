from app.unit_of_work import UnitOfWork
from datetime import datetime

async def mark_borrow_as_overdue(uow_factory):
    async with uow_factory() as uow:
        now = datetime.utcnow()
        borrows = await uow.borrow.get_owerdue_by_date(now=now)
        await uow.borrow.mark_many_as_overdue(borrows=borrows)