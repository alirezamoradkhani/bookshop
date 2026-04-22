from sqlalchemy.ext.asyncio import AsyncSession
from app.user.repo.baseuser import BaseUserRepository
from app.user.repo.user import UserRepository
from app.user.repo.author import AuthorRepository
from app.user.repo.admin import AdminRepository
from app.book.repo.book import BookRepository
from app.book.repo.book_author import BookAuthorRepository
from app.edition.repo.edition import EditionRepository
from app.order.repo.order import OrderRepository
from app.order.repo.order_edition import OrderEditionRepository
from app.transaction.repo.transaction import TransactionRepository
from app.borrow.repo.borrow import Borrowpository

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
        self.edition = EditionRepository(db)
        self.order = OrderRepository(db)
        self.orderedition = OrderEditionRepository(db)
        self.admin = AdminRepository
        self.transaction = TransactionRepository(db)
        self.borrow = Borrowpository(db)

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
