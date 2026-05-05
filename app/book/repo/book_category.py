from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.book.models import model

class BookCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, book_category:model.BookCategory):
        self.db.add(book_category)

    async def delete(self, book_category:model.BookCategory):
        await self.db.delete(book_category)

    async def get_by_book_id(self,book_id:int):
        result = await self.db.execute(select(model.BookCategory).where(model.BookCategory.book_id == book_id))
        return result.scalars().all()