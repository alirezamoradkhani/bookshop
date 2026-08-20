from fastapi import APIRouter, Depends, Request
from app.core.security import get_current_user
from app.borrow.schemas.outputs import WaitlistResponse, BorrowResponse
from app.borrow.services.borrow.borrow_edition import borrow_edition, get_user_borrows
from app.borrow.services.borrow.return_borrow import return_borrow
from app.borrow.services.wait_list.create_waitlist import add_to_wait_list
from app.ratelimiter.limiter import limiter
from dependency_injector.wiring import inject, Provide
from app.dependency_injection.container import Container


router = APIRouter(prefix="/borrows", tags=["borrows"])

@router.get("/user", response_model=list[BorrowResponse])
@limiter.limit("5/minute")
@inject
async def List_borrows(request: Request, uow = Depends(Provide[Container.uow]), token_data = Depends(get_current_user)):
    return await get_user_borrows(uow=uow, token_data=token_data)

@router.post("/take", response_model=BorrowResponse)
@limiter.limit("5/minute")
@inject
async def Borrow_edition(request: Request, edition_id:int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await borrow_edition(uow=uow,token_data=token_data,edition_id=edition_id)

@router.post("/return", response_model=BorrowResponse)
@limiter.limit("5/minute")
@inject
async def Return_borrow(request: Request, borrow_id:int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await return_borrow(uow=uow,token_data=token_data,borrow_id=borrow_id)

@router.post("/waitlist", response_model=WaitlistResponse)
@limiter.limit("5/minute")
@inject
async def Add_to_waitlist(request: Request, edition_id:int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await add_to_wait_list(uow=uow,token_data=token_data,edition_id=edition_id)
