from app.unit_of_work import UnitOfWork

class OrderCreateConsumer:
    async def handle(self, event: dict, uow:UnitOfWork):
        pass