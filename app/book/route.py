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

@router.get("details",response_model=outputs.BookDetails)
async def get_detail(book_id:int,uow = Depends(get_uow)):
    return await book_detail(uow=uow,book_id=book_id)