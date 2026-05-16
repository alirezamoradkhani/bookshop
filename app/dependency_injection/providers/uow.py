from sqlalchemy.ext.asyncio import AsyncSession
from app.unit_of_work import UnitOfWork


def uow_factory(session: AsyncSession):
    return UnitOfWork(session)