import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org"

    def __init__(self, http_client: httpx.AsyncClient, user_agent):
        self._http = http_client
        self._user_agent = user_agent

    def _retry_policy(self):
        return retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(min=1, max=5),
            retry=retry_if_exception_type(
                (httpx.TimeoutException, httpx.RequestError)
            ),
            reraise=True
        )

    @property
    def _request(self):
        return self._retry_policy()(self._http.get)

    async def search_books(self, query: str):
        url = f"{self.BASE_URL}/search.json"
        response = await self._request(url, params={"q": query}, timeout=10)
        response.raise_for_status()
        return response.json()

    async def search_books_by_title(self, title: str):
        url = f"{self.BASE_URL}/search.json"
        response = await self._request(url, params={"title": title}, timeout=10)
        response.raise_for_status()
        return response.json()

    async def search_books_by_author(self, author: str):
        url = f"{self.BASE_URL}/search.json"
        response = await self._request(url, params={"author": author}, timeout=10)
        response.raise_for_status()
        return response.json()

    async def search_books_by_isbn(self, isbn: str):
        url = f"{self.BASE_URL}/search.json"
        response = await self._request(url, params={"isbn": isbn}, timeout=10)
        response.raise_for_status()
        return response.json()

    async def get_work(self, work_id: str):
        url = f"{self.BASE_URL}/works/{work_id}.json"
        response = await self._request(url, timeout=10)
        response.raise_for_status()
        return response.json()