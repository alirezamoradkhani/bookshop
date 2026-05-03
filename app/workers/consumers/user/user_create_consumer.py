from app.unit_of_work import UnitOfWork

class UserCreateConsumer:
    async def handle(self, event: dict, uow:UnitOfWork):
        pass