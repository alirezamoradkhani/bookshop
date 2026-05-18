from app.unit_of_work import UnitOfWork

class EditionIndexer:

    def __init__(self, provider, uow: UnitOfWork):
        self.provider = provider
        self.uow = uow
        
    async def index_edition(self, edition_id:int):
        edition = await self.uow.edition.get_by_id(edition_id)
        if not edition:
            return
        book = await self.uow.book.get_by_id(edition.book_id)
        if not book:
            return
        doc = {
            "id": edition.id,
            "edition_title": edition.specefic_edition_title,
            "isbn": edition.isbn,
            "description": edition.description,
            "price": edition.price,
            "amount": edition.amount,
            "purchasable": edition.amount>=0 and not edition.is_deleted and not book.is_deleted,
            "book_id": book.id,
            "book_title": book.title,
            "book_author_names": [a.username for a in await self.uow.author.get_by_ids([b.author_id for b in await self.uow.bookauthor.get_by_book_id(book.id)])],
            "book_category": [c.category for c in await self.uow.bookcategory.get_by_book_id(book.id)],
            "available": not edition.is_deleted and not book.is_deleted
        }
        
        await self.provider.index(index_name="editions", doc=doc)

    async def delete_edition(self, edition_id: int):
        await self.provider.delete(index_name="editions", doc_id=str(edition_id))