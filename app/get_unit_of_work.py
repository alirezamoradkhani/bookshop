from app.unit_of_work import UnitOfWork
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_uow(db: AsyncSession = Depends(get_db)):
    uow = UnitOfWork(db)
    yield uow