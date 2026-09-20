from app.mongo.database import MongoContext
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
    def __init__(self, db: MongoContext):
        self.db = db
        self.baseusers = BaseUserRepository(db)
        self.user = UserRepository(db)
        self.author = AuthorRepository(db)
        self.book = BookRepository(db)
        self.bookauthor = BookAuthorRepository(db)
        self.bookcategory = BookCategoryRepository(db)
        self.edition = EditionRepository(db)
        self.editionlanguage = EditionLanguageRepository(db)
        self.order = OrderRepository(db)
        self.orderedition = OrderEditionRepository(db)
        self.admin = AdminRepository(db)
        self.transaction = TransactionRepository(db)
        self.borrow = Borrowpository(db)
        self.waitlist = Waitlistpository(db)
        self.outbox = OutboxRepository(db)

    async def __aenter__(self):
        await self.db.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return await self.db.__aexit__(exc_type, exc, tb)

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, obj):
        return obj

    async def flush(self):
        await self.db.flush()
