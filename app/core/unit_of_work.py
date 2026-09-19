from app.mongo.database import MongoContext
from app.mongo.repositories import (
    AdminRepository,
    AuthorRepository,
    BaseUserRepository,
    BookAuthorRepository,
    BookCategoryRepository,
    BookRepository,
    Borrowpository,
    EditionLanguageRepository,
    EditionRepository,
    OrderEditionRepository,
    OrderRepository,
    OutboxRepository,
    TransactionRepository,
    UserRepository,
    Waitlistpository,
)


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
