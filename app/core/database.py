from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.setting import settings

client: AsyncMongoClient = AsyncMongoClient(settings.mongo_url)
database: AsyncDatabase = client[settings.mongo_database]

async def init_mongo() -> None:
    await database.command("ping")
    await database.users.create_index("email", unique=True)
    await database.users.create_index([("username", 1), ("is_deleted", 1)])
    await database.books.create_index("title")
    await database.books.create_index("author_ids")
    await database.books.create_index("categories")
    await database.book_authors.create_index([("book_id", 1), ("author_id", 1)], unique=True)
    await database.book_categories.create_index([("book_id", 1), ("category", 1)], unique=True)
    await database.edition_languages.create_index([("edition_id", 1), ("language", 1)], unique=True)
    await database.editions.create_index("book_id")
    await database.orders.create_index("user_id")
    await database.orders.create_index("state")
    await database.order_editions.create_index("order_id")
    await database.order_editions.create_index("edition_id")
    await database.borrows.create_index([("user_id", 1), ("edition_id", 1), ("status", 1)])
    await database.waitlist.create_index([("user_id", 1), ("edition_id", 1)], unique=True)
    await database.transactions.create_index([("user_id", 1), ("date", -1)])
    await database.outbox_events.create_index([("processed", 1), ("id", 1)])
