from app.mongo.base import MongoRepository
from app.book.models.model import Book
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class BookRepository(MongoRepository):
    collection, model = "books", Book

    async def create_book(self, new_book: Book):
        return await self._insert(new_book)

    async def get_by_id(self, id: int):
        return await self._find_one({"_id": id, "is_deleted": False})

    async def get_by_external_id(self, external_provider: str, external_id: str):
        return await self._find_one({"external_provider": external_provider, "external_id": external_id})

    async def update_book_title(self, book: Book, title: str):
        book.title = title

    async def delete_book(self, book: Book):
        book.is_deleted = True

    async def search_books(self, title=None, category=None, author_id=None):
        query: dict[str, Any] = {"is_deleted": False}
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if category:
            query["categories"] = category
        if author_id:
            query["author_ids"] = author_id
        return await self._find(query)

    async def get_all(self):
        return await self._find({"is_deleted": False})
