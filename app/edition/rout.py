from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.edition.schemas.inputs import EditionCreate
from app.edition.services.create_edition import create_edition
from app.edition.services.update_amount import update_amount
from app.edition.services.update_price import update_price


router = APIRouter(prefix="/editions", tags=["editions"])

@router.post("/create")
async def add_edition(edition: EditionCreate,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await create_edition(uow=uow,token_data=token_data,edition=edition)

@router.patch("/amount")
async def change_amount(new_amount: int,edition_id : int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await update_amount(uow=uow,token_data=token_data,new_amount=new_amount,edition_id=edition_id)

@router.patch("/price")
async def change_price(new_price: int,edition_id : int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await update_price(uow=uow,token_data=token_data,new_price=new_price,edition_id=edition_id)