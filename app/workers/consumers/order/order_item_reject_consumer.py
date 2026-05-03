from app.unit_of_work import UnitOfWork

class OrderItemRejectConsumer:
    async def handle(self, event: dict, uow:UnitOfWork):
        pass