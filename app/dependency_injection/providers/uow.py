from app.core.unit_of_work import UnitOfWork
from app.mongo.database import MongoContext


def uow_factory(session: MongoContext) -> UnitOfWork:
    return UnitOfWork(session)
