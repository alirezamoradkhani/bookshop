from app.unit_of_work import UnitOfWork
from app.borrow.models import enums
from datetime import datetime, timedelta

async def mark_borrow_as_overdue(uow: UnitOfWork):
    now = datetime.utcnow()
    borrows = await uow.borrow.get_owerdue_by_date(now=now)
    for borrow in borrows:
        await uow.borrow.update_status(borrow=borrow,new_status=enums.BorrowStatus.OVERDUE)