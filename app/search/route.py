from fastapi import APIRouter,Depends
from app.search.service.search_book import search_books
from dependency_injector.wiring import inject, Provide
from app.dependency_injection.container import Container


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("")
@inject
async def search(
    q: str,
    author_id: int | None = None,
    category: str | None = None,
    page: int = 1,
    size: int = 20,
    search_provider = Depends(Provide[Container.search_provider])
):
    return await search_books(
        q=q,
        author_id=author_id,
        category=category
        ,search_provider=search_provider
        ,page=page
        ,size=size)