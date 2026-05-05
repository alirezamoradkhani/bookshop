from app.unit_of_work import UnitOfWork
from datetime import datetime

async def mark_borrow_as_overdue(uow: UnitOfWork):
    now = datetime.utcnow()
    borrows = await uow.borrow.get_owerdue_by_date(now=now)
    for borrow in borrows:
        await uow.borrow.mark_as_owerdue(borrow=borrow)