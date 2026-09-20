from app.mongo.base import MongoRepository
from app.book.models.model import BookAuthor
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class BookAuthorRepository(MongoRepository):
    collection, model = "book_authors", BookAuthor

    async def create(self, book_author: BookAuthor):
        return await self._insert(book_author)

    async def create_many(self, items: list[BookAuthor]):
        for item in items:
            await self._insert(item)
            await self.db.collection("books").update_one(
                {"_id": item.book_id}, {"$addToSet": {"author_ids": item.author_id}}, **self.db.options()
            )

    async def get_by_authorid_and_bookid(self, book_id: int, author_id: int):
        return await self._find_one({"book_id": book_id, "author_id": author_id})

    async def get_by_author_id(self, author_id):
        return await self._find({"author_id": author_id})

    async def get_by_book_id(self, book_id: int):
        return await self._find({"book_id": book_id})

    async def get_by_book_ids(self, book_ids: list[int]):
        return await self._find({"book_id": {"$in": book_ids}})

    async def count_of_author(self, book_id: int):
        return len(await self.get_by_book_id(book_id))
