from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.book.models import model

class BookAuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, book_author:model.BookAuthor):
        self.db.add(book_author)

    async def get_by_authorid_and_bookid(self,book_id:int, author_id:int):
        result = await self.db.execute(select(model.BookAuthor).where(model.BookAuthor.author_id == author_id,model.BookAuthor.book_id == book_id))
        return result.scalar_one_or_none()

    async def get_by_author_id(self,author_id):
        result = await self.db.execute(select(model.BookAuthor).where(model.BookAuthor.author_id == author_id))
        return result.scalars().all()