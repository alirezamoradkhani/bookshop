from app.external_API.providers.open_library.service import OpenLibraryProvider


async def external_search_book_by_ISBN(provider:OpenLibraryProvider,isbn:str):
    return await provider.search_by_isbn(isbn=isbn)