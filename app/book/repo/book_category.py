from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.book.models import model

class BookCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, book_category:model.BookCategory):
        self.db.add(book_category)

    async def create_many(self, items: list[model.BookCategory]):
        self.db.add_all(items)

    async def delete(self, book_category:model.BookCategory):
        await self.db.delete(book_category)

    async def get_by_book_id(self,book_id:int):
        result = await self.db.execute(select(model.BookCategory).where(model.BookCategory.book_id == book_id))
        return result.scalars().all()
    
    async def delete_by_book_id(self, book_id: int):
        await self.db.execute(delete(model.BookCategory).where(model.BookCategory.book_id == book_id))