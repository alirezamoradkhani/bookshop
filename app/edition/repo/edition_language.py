from app.mongo.base import MongoRepository
from app.edition.models.model import EditionLanguage
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class EditionLanguageRepository(MongoRepository):
    collection, model = "edition_languages", EditionLanguage

    async def create(self, edition_language: EditionLanguage):
        return await self._insert(edition_language)

    async def create_many(self, items: list[EditionLanguage]):
        for item in items:
            await self._insert(item)
