from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.book.models import model

class BookAuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self,author_ids: list[int],book_id: int):
        for author_id in author_ids:
            book_author = model.BookAuthor(book_id=book_id,author_id= author_id)
            self.db.add(book_author)

    
    async def get_bookauthor_by_author_id(self,author_id):
        result = await self.db.execute(select(model.BookAuthor).where(model.BookAuthor.author_id == author_id))
        return result.scalars().all()