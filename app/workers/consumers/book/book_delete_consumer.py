from app.unit_of_work import UnitOfWork

class BookDeleteConsumer:
    async def handle(self, event: dict, uow:UnitOfWork):
        pass