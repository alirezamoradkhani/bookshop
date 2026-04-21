from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.order.serivices.create_oreder import create_order
from app.order.schemas.outputs import OrderResponse


router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/buy",response_model= OrderResponse)
async def buy(edition_ids: list[int] ,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await create_order(uow=uow,token_data=token_data,edition_ids=edition_ids)