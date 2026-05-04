from app.external_API.providers.open_library.service import OpenLibraryProvider


async def external_book_detail_by_id(provider:OpenLibraryProvider,work_id:str ):
    return await provider.get_work(work_id=work_id)