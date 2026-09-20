from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.unit_of_work import UnitOfWork


def uow_factory(database: AsyncDatabase, client: AsyncMongoClient) -> UnitOfWork:
    return UnitOfWork(database, client)
