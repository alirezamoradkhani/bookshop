from app.unit_of_work import UnitOfWork

class BorrowOverdueConsumer:
    async def handle(self, event: dict, uow:UnitOfWork):
        pass