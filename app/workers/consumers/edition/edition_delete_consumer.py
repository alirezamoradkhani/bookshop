from app.core.unit_of_work import UnitOfWork
from app.workers.consumers.base import BaseConsumer
from app.workers.consumers.base import container
from app.search.indexer.edition_indexer import EditionIndexer

class EditionDeleteConsumer(BaseConsumer):
    event_type = "EditionDeleted"
    async def process(self, event: dict, uow:UnitOfWork):
        edition_id = event["edition_id"]
        provider = container.search_provider()
        indexer = EditionIndexer(provider=provider, uow=uow)
        await indexer.delete_edition(edition_id)