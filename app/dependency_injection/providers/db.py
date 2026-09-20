from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.database import client, database


def get_database() -> AsyncDatabase:
    return database


def get_client() -> AsyncMongoClient:
    return client
