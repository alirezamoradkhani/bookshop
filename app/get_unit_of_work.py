from app.database import SessionLocal
from app.unit_of_work import UnitOfWork

async def get_uow():
    async with SessionLocal() as db:
        yield UnitOfWork(db)