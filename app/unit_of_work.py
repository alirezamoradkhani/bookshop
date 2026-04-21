from sqlalchemy.ext.asyncio import AsyncSession
from app.user.repo.baseuser import BaseUserRepository
from app.user.repo.user import UserRepository
from app.user.repo.author import AuthorRepository
from app.book.repo.book import BookRepository
from app.book.repo.book_author import BookAuthorRepository
from app.database import get_db
from fastapi import Depends

class UnitOfWork:
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.baseusers = BaseUserRepository(db)
        self.user = UserRepository(db)
        self.author = AuthorRepository(db)
        self.book = BookRepository(db)
        self.bookauthor = BookAuthorRepository(db)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, obj):
        await self.db.refresh(obj)
    async def flush(self):
        await self.db.flush()
