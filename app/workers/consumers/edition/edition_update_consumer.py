from app.unit_of_work import UnitOfWork

class EditionUpdateConsumer:
    async def handle(self, event: dict, uow:UnitOfWork):
        pass