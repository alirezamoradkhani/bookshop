from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.book.schemas import inputs, outputs
from app.book.services.create_book import create_book
from app.book.services.update_book import update_book
from app.book.services.delete_book import delete_book


router = APIRouter(prefix="/books", tags=["books"])

@router.post("add",response_model=outputs.BookResponse)
async def add_book(new_book:inputs.BookCreate,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await create_book(uow=uow,new_book=new_book,token_data=toke_data)

@router.patch("update", response_model= outputs.BookResponse)
async def Update_book(book_id :int,book_update:inputs.BookUpdate,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await update_book(uow=uow,token_data=toke_data,book_id=book_id,book_update=book_update)

@router.delete("/",response_model=outputs.BookResponse)
async def remove_book(book_id: int,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await delete_book(uow=uow,token_data=toke_data,book_id=book_id)
