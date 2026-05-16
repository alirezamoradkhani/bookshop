from app.external_API.providers.open_library.service import OpenLibraryProvider


async def external_search_book_by_title(provider:OpenLibraryProvider,title:str):
    return await provider.search_by_title(title=title)