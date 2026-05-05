from app.unit_of_work import UnitOfWork

async def search_books(uow: UnitOfWork
                ,title: str | None = None
                ,author_id: int | None = None
                ,category: str | None = None):
    async with uow:
        books = await uow.book.search_books(
            title=title,
            category=category,
            author_id=author_id
        )
        return books