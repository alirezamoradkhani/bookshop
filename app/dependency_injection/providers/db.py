from app.core.database import client, database
from app.mongo.database import MongoContext


def create_session() -> MongoContext:
    return MongoContext(database, client)


async def get_session():
    yield create_session()
