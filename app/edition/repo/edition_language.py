from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.edition.models.model import EditionLanguage


class EditionLanguageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self,edition_language:EditionLanguage):
        self.db.add(edition_language)