import httpx
from app.external_API.providers.open_library.client import OpenLibraryClient
from app.external_API.providers.open_library.mapper import OpenLibraryMapper
from app.external_API.interfaces.book_providers import BookProvider
from app.exceptions.models.external_service import ExternalServiceError,ExternalServiceTimeout,ExternalServiceUnavailable


class OpenLibraryProvider(BookProvider):

    def __init__(self, client: OpenLibraryClient):
        self.client = client

    async def _safe_call(self, func, *args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except httpx.TimeoutException:
            raise ExternalServiceTimeout()

        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500:
                raise ExternalServiceUnavailable()
            raise ExternalServiceError()

        except httpx.RequestError:
            raise ExternalServiceUnavailable()

        except ValueError:
            raise ExternalServiceError()

    async def search_by_title(self, title: str):
        raw = await self._safe_call(self.client.search_books_by_title, title)

        return [
            OpenLibraryMapper.map_search_result(doc)
            for doc in raw.get("docs", [])
        ]

    async def search_by_author(self, author: str):
        raw = await self._safe_call(self.client.search_books_by_author, author)

        return [
            OpenLibraryMapper.map_search_result(doc)
            for doc in raw.get("docs", [])
        ]

    async def search_by_isbn(self, isbn: str):
        raw = await self._safe_call(self.client.search_books_by_isbn, isbn)

        return [
            OpenLibraryMapper.map_search_result(doc)
            for doc in raw.get("docs", [])
        ]

    async def get_work(self, work_id: str):
        raw = await self._safe_call(self.client.get_work, work_id)

        return OpenLibraryMapper.map_work_result(raw)