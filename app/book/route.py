from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
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

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/",response_model=outputs.BookResponse)
async def add_book(new_book:inputs.BookCreate,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await create_book(uow=uow,new_book=new_book,token_data=toke_data)

@router.patch("/", response_model= outputs.BookResponse)
async def Update_book(book_id :int,book_update:inputs.BookUpdate,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await update_book(uow=uow,token_data=toke_data,book_id=book_id,book_update=book_update)

@router.delete("/",response_model=outputs.BookResponse)
async def remove_book(book_id: int,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await delete_book(uow=uow,token_data=toke_data,book_id=book_id)

@router.get("/search",response_model= list[outputs.BookResponse])
async def Search_book(category: str | None = None
                ,author_id: int | None = None
                ,title: str | None = None,uow = Depends(get_uow)):
    return await search_books(uow=uow,category=category,title=title,author_id=author_id)

@router.get("/details",response_model=outputs.BookDetails)
async def get_detail(book_id:int,uow = Depends(get_uow)):
    return await book_detail(uow=uow,book_id=book_id)

@router.get("/external/search/by_title")
async def External_search_book_by_title(title:str, provider = Depends(get_openlibrary_provider)):
    return await external_search_book_by_title(title=title, provider=provider)

@router.get("/external/search/by_author")
async def External_search_book_by_author(author:str, provider = Depends(get_openlibrary_provider)):
    return await external_search_book_by_author(author=author, provider=provider)

@router.get("/external/search/by_isbn")
async def External_search_book_by_isbn(isbn:str, provider = Depends(get_openlibrary_provider)):
    return await external_search_book_by_ISBN(isbn=isbn, provider=provider)

@router.get("/external/detail_by_id")
async def External_book_detail_by_id(book_id:str, provider = Depends(get_openlibrary_provider)):
    return await external_book_detail_by_id(provider=provider,work_id=book_id)

@router.post("/external")
async def import_book_by_name(book_title:str ,uow = Depends(get_uow),toke_data = Depends(get_current_user),provider = Depends(get_openlibrary_provider)):
    return await import_book(uow=uow,book_title=book_title,token_data=toke_data,provider=provider)