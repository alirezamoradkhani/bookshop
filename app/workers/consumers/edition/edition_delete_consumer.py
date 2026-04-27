from app.unit_of_work import UnitOfWork

class EditionDeleteConsumer:
    async def handle(self, event: dict, uow:UnitOfWork):
        pass