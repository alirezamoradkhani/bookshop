from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer
from app.workers.consumers.base import container
from app.search.indexer.book_indexer import BookIndexer

class BookUpdateConsumer(BaseConsumer):
    event_type = "BookUpdated"
    async def process(self, event: dict, uow:UnitOfWork):

        book_id = event["book_id"]
        provider = container.search_provider()
        indexer = BookIndexer(provider=provider, uow=uow)
        await indexer.index_book(book_id)