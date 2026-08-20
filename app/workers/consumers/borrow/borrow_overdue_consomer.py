from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer

class BorrowOverdueConsumer(BaseConsumer):
    event_type = "BorrowOverdue"
    async def process(self, event: dict, uow:UnitOfWork):
        borrow_id = event.get("borrow_id")
        if borrow_id is None or await uow.borrow.get_by_id(borrow_id) is None:
            raise ValueError(f"BorrowOverdue references missing borrow {borrow_id}")
