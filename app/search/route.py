from fastapi import APIRouter, Depends, Query
from app.search.service.book.search_book import search_books
from app.search.service.edition.search_edition import search_editions
from dependency_injector.wiring import inject, Provide
from app.dependency_injection.container import Container


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/book")
@inject
async def search_book(
    q: str = Query(min_length=1, max_length=200),
    author_id: int | None = None,
    category: str | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
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
async def search_edition(q: str = Query(min_length=1, max_length=200),
    book_id: int | None = None,
    category: str | None = None,
    available:bool | None=None,
    purchasable:bool | None=None,
    min_price: int | None = Query(default=None, ge=0),
    max_price: int | None = Query(default=None, ge=0),
    search_provider = Depends(Provide[Container.search_provider]),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100)
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
