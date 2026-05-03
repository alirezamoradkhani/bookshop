from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.borrow.schemas.outputs import WaitlistResponse
from app.borrow.services.borrow.borrow_edition import borrow_edition
from app.borrow.services.borrow.return_borrow import return_borrow
from app.borrow.services.wait_list.create_waitlist import add_to_wait_list


router = APIRouter(prefix="/borrows", tags=["borrows"])

@router.post("/take")
async def Borrow_edition(edition_id:int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await borrow_edition(uow=uow,token_data=token_data,edition_id=edition_id)

@router.post("/return")
async def Return_borrow(borrow_id:int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await return_borrow(uow=uow,token_data=token_data,borrow_id=borrow_id)

@router.post("/waitlist", response_model=WaitlistResponse)
async def Add_to_waitlist(edition_id:int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await add_to_wait_list(uow=uow,token_data=token_data,edition_id=edition_id)