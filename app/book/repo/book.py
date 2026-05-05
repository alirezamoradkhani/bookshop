from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.book.models import model, enums

class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book(self,new_book:model.Book):
        self.db.add(new_book)
        return new_book
    
    async def get_by_id(self,id:int):
        result = await self.db.execute(select(model.Book).where(model.Book.id == id))
        return result.scalar_one_or_none()

    async def update_book_title(self,book:model.Book,title:str):
        book.title = title

    async def update_book_category(self,book:model.Book,category:enums.Category):
        book.category = category
    
    async def delete_book(self,book:model.Book):
        book.is_deleted = True

    async def search_books(self, title=None, category=None, author_id=None):
        result = select(model.Book).where(model.Book.is_deleted == False)
        
        if title:
            result = result.where(model.Book.title.ilike(f"%{title}%"))
        if author_id:
            result = result.join(model.BookAuthor,model.BookAuthor.book_id == model.Book.id).where(model.BookAuthor.author_id == author_id)
        if category:
            result = result.join(model.BookCategory).where(model.BookCategory.category == category)
        
        result = await self.db.execute(result)
        return result.scalars().all()