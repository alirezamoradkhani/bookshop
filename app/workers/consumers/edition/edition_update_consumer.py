from app.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer
from app.workers.consumers.base import container
from app.search.indexer.edition_indexer import EditionIndexer

class EditionUpdateConsumer(BaseConsumer):
    event_type = "EditionUpdated"
    async def process(self, event: dict, uow:UnitOfWork):
        edition_id = event["edition_id"]
        provider = container.search_provider()
        indexer = EditionIndexer(provider=provider, uow=uow)
        await indexer.index_edition(edition_id)