from fastapi import APIRouter,Depends
from app.search.service.book.search_book import search_books
from app.search.service.edition.search_edition import search_editions
from dependency_injector.wiring import inject, Provide
from app.dependency_injection.container import Container


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/book")
@inject
async def search_book(
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

@router.get("/edition")
@inject
async def search_edition(q: str,
    book_id=None,
    category=None,
    available:bool | None=None,
    purchasable:bool | None=None,
    min_price=None,
    max_price=None,
    search_provider = Depends(Provide[Container.search_provider]),
    page: int = 1,
    size: int = 20
):
    return await search_editions(
        available=available,
        book_id=book_id,
        category=category,
        max_price=max_price,
        min_price=min_price,
        page=page,
        purchasable=purchasable,
        q=q,
        search_provider=search_provider,
        size=size)