from app.unit_of_work import UnitOfWork

class BookIndexer:

    def __init__(self, provider, uow: UnitOfWork):
        self.provider = provider
        self.uow = uow

    async def index_book(self, book_id:int):
        book = await self.uow.book.get_by_id(book_id)
        if not book:
            return
        doc = {
            "id": book.id,
            "title": book.title,
            "author_name": [a.username for a in await self.uow.author.get_by_ids([b.author_id for b in await self.uow.bookauthor.get_by_book_id(book.id)])],
            "category": [c.category for c in await self.uow.bookcategory.get_by_book_id(book.id)],
            "available": not book.is_deleted
        }

        await self.provider.index(index_name="books", doc=doc)

    async def delete_book(self, book_id: int):
        await self.provider.delete(index_name="books", doc_id=str(book_id))