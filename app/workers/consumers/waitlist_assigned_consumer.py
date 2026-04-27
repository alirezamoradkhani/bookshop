from app.unit_of_work import UnitOfWork

class WaitlistAssigneConsumer:
    async def handle(self, event: dict, uow:UnitOfWork):
        pass