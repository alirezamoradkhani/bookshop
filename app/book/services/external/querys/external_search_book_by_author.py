from app.external_API.providers.open_library.service import OpenLibraryProvider


async def external_search_book_by_author(provider:OpenLibraryProvider,author:str):
    return await provider.search_by_author(author=author)