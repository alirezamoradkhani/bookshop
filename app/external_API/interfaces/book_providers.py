from typing import List
from app.external_API.providers.open_library.dto import ExternalBookDTO


class BookProvider:

    async def search_by_title(self, title: str) -> List[ExternalBookDTO]:
        raise NotImplementedError

    async def search_by_author(self, author: str) -> List[ExternalBookDTO]:
        raise NotImplementedError

    async def search_by_isbn(self, isbn: str) -> List[ExternalBookDTO]:
        raise NotImplementedError

    async def get_work(self, work_id: str) -> ExternalBookDTO:
        raise NotImplementedError