import httpx
from app.external_API.providers.open_library.client import OpenLibraryClient
from app.external_API.providers.open_library.service import OpenLibraryProvider


async def openlibrary_http_client():
    async with httpx.AsyncClient() as client:
        yield client



def openlibrary_provider(http_client: httpx.AsyncClient):
    client = OpenLibraryClient(
        http_client=http_client,
        user_agent="BookStoreApp/1.0 (contact: you@example.com)"
    )

    return OpenLibraryProvider(client=client)