from sqlalchemy.ext.asyncio import AsyncSession
from app.core.unit_of_work import UnitOfWork


def uow_factory(session: AsyncSession):
    return UnitOfWork(session)