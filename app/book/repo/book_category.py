from app.mongo.base import MongoRepository
from app.book.models.model import BookCategory
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class BookCategoryRepository(MongoRepository):
    collection, model = "book_categories", BookCategory

    async def create(self, book_category: BookCategory):
        return await self._insert(book_category)

    async def create_many(self, items: list[BookCategory]):
        for item in items:
            await self._insert(item)
            await self.db.collection("books").update_one(
                {"_id": item.book_id}, {"$addToSet": {"categories": item.category}}, **self.db.options()
            )

    async def delete(self, book_category: BookCategory):
        await self._delete(book_category)
        await self.db.collection("books").update_one(
            {"_id": book_category.book_id}, {"$pull": {"categories": book_category.category}}, **self.db.options()
        )

    async def get_by_book_id(self, book_id: int):
        return await self._find({"book_id": book_id})

    async def delete_by_book_id(self, book_id: int):
        await self.db.collection(self.collection).delete_many({"book_id": book_id}, **self.db.options())
        await self.db.collection("books").update_one({"_id": book_id}, {"$set": {"categories": []}}, **self.db.options())
