from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.book.schemas import inputs, outputs
from app.book.services.create_book import create_book


router = APIRouter(prefix="/books", tags=["books"])

@router.post("add",response_model=outputs.BookResponse)
async def add_book(new_book:inputs.BookCreate,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await create_book(uow=uow,new_book=new_book,token_data=toke_data)