from fastapi import APIRouter, Depends, Request
from app.security import get_current_user
from app.book.schemas import inputs, outputs
from app.book.models.enums import Category
from app.book.services.command.create_book import create_book
from app.book.services.command.update_book import update_book
from app.book.services.command.delete_book import delete_book
from app.book.services.querys.search_book import search_books
from app.book.services.querys.get_book_details import book_detail
from app.book.services.external.querys.external_search_book_by_title import external_search_book_by_title
from app.book.services.external.querys.external_search_book_by_author import external_search_book_by_author
from app.book.services.external.querys.external_search_book_by_ISBN import external_search_book_by_ISBN
from app.book.services.external.querys.external_book_detail_by_id import external_book_detail_by_id
from app.external_API.providers.open_library.get_extternal_services import get_openlibrary_provider
from app.book.services.external.command.import_external_book import import_book
from app.ratelimiter.limiter import limiter
from dependency_injector.wiring import inject, Provide
from app.dependency_injection.container import Container


router = APIRouter(prefix="/books", tags=["books"])

@router.post("/",response_model=outputs.BookResponse)
@limiter.limit("5/minute")
@inject
async def add_book(request: Request,new_book:inputs.BookCreate,uow = Depends(Provide[Container.uow]),toke_data = Depends(get_current_user)):
    return await create_book(uow=uow,new_book=new_book,token_data=toke_data)

@router.patch("/", response_model= outputs.BookResponse)
@limiter.limit("5/minute")
@inject
async def Update_book(request: Request,book_id :int,book_update:inputs.BookUpdate,uow = Depends(Provide[Container.uow]),toke_data = Depends(get_current_user)):
    return await update_book(uow=uow,token_data=toke_data,book_id=book_id,book_update=book_update)

@router.delete("/",response_model=outputs.BookResponse)
@limiter.limit("5/minute")
@inject
async def remove_book(request: Request,book_id: int,uow = Depends(Provide[Container.uow]),toke_data = Depends(get_current_user)):
    return await delete_book(uow=uow,token_data=toke_data,book_id=book_id)

@router.get("/search",response_model= list[outputs.BookResponse])
@limiter.limit("5/minute")
@inject
async def Search_book(request: Request
                ,category: str | None = None
                ,author_id: int | None = None
                ,title: str | None = None,uow = Depends(Provide[Container.uow])):
    return await search_books(uow=uow,category=category,title=title,author_id=author_id)

@router.get("/details",response_model=outputs.BookDetails)
@limiter.limit("5/minute")
@inject
async def get_detail(request: Request,book_id:int,uow = Depends(Provide[Container.uow])):
    return await book_detail(uow=uow,book_id=book_id)

@router.get("/external/search/by_title")
@limiter.limit("5/minute")
@inject
async def External_search_book_by_title(request: Request, title:str, provider = Depends(Provide[Container.openlibrary])):
    return await external_search_book_by_title(title=title, provider=provider)

@router.get("/external/search/by_author")
@limiter.limit("5/minute")
@inject
async def External_search_book_by_author(request: Request, author:str, provider = Depends(Provide[Container.openlibrary])):
    return await external_search_book_by_author(author=author, provider=provider)

@router.get("/external/search/by_isbn")
@limiter.limit("5/minute")
@inject
async def External_search_book_by_isbn(request: Request, isbn:str, provider = Depends(Provide[Container.openlibrary])):
    return await external_search_book_by_ISBN(isbn=isbn, provider=provider)

@router.get("/external/detail_by_id")
@limiter.limit("5/minute")
@inject
async def External_book_detail_by_id(request: Request, book_id:str, provider = Depends(Provide[Container.openlibrary])):
    return await external_book_detail_by_id(provider=provider,work_id=book_id)

@router.post("/external")
@limiter.limit("5/minute")
@inject
async def import_book_by_name(request: Request, ext_book_id:str ,uow = Depends(Provide[Container.uow]),toke_data = Depends(get_current_user),provider = Depends(Provide[Container.openlibrary])):
    return await import_book(uow=uow,ext_book_id=ext_book_id,token_data=toke_data,provider=provider)