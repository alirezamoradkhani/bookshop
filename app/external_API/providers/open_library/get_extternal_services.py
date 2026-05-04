import httpx
from app.external_API.providers.open_library.client import OpenLibraryClient
from app.external_API.providers.open_library.service import OpenLibraryProvider


async def get_openlibrary_provider():
    async with httpx.AsyncClient() as http_client:
        client = OpenLibraryClient(
            http_client=http_client,
            user_agent="BookStoreApp/1.0 (contact: you@example.com)"
        )

        yield OpenLibraryProvider(client=client)