from typing import Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.setting import settings
from app.user.repo.baseuser import BaseUserRepository
from app.user.repo.user import UserRepository
from app.user.repo.author import AuthorRepository
from app.user.repo.admin import AdminRepository
from app.book.repo.book import BookRepository
from app.book.repo.book_author import BookAuthorRepository
from app.book.repo.book_category import BookCategoryRepository
from app.edition.repo.edition import EditionRepository
from app.edition.repo.edition_language import EditionLanguageRepository
from app.order.repo.order import OrderRepository
from app.order.repo.order_edition import OrderEditionRepository
from app.borrow.repo.borrow import Borrowpository
from app.borrow.repo.waitlist import Waitlistpository
from app.transaction.repo.transaction import TransactionRepository
from app.outbox.repo import OutboxRepository


class UnitOfWork:
    def __init__(self, database: AsyncDatabase, client: AsyncMongoClient):
        self.db = database
        self.client = client
        self.session: Any = None
        session_provider = lambda: self.session
        self.baseusers = BaseUserRepository(database, session_provider)
        self.user = UserRepository(database, session_provider)
        self.author = AuthorRepository(database, session_provider)
        self.book = BookRepository(database, session_provider)
        self.bookauthor = BookAuthorRepository(database, session_provider)
        self.bookcategory = BookCategoryRepository(database, session_provider)
        self.edition = EditionRepository(database, session_provider)
        self.editionlanguage = EditionLanguageRepository(database, session_provider)
        self.order = OrderRepository(database, session_provider)
        self.orderedition = OrderEditionRepository(database, session_provider)
        self.admin = AdminRepository(database, session_provider)
        self.transaction = TransactionRepository(database, session_provider)
        self.borrow = Borrowpository(database, session_provider)
        self.waitlist = Waitlistpository(database, session_provider)
        self.outbox = OutboxRepository(database, session_provider)

    async def __aenter__(self):
        if settings.mongo_transactions:
            self.session = await self.client.start_session()
            self.session.start_transaction()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            if self.session is not None:
                await self.session.end_session()
                self.session = None

    async def commit(self):
        if self.session is not None and self.session.in_transaction:
            await self.session.commit_transaction()

    async def rollback(self):
        if self.session is not None and self.session.in_transaction:
            await self.session.abort_transaction()
