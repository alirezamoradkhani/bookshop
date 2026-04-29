from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.order.serivices.user.command.create_oreder import create_order
from app.order.serivices.user.command.cancel_order import cancel_order
from app.order.serivices.author.querys.get_orderedition import get_order_edition
from app.order.serivices.author.command.accept_order_edition import accept_order_edition
from app.order.serivices.author.command.reject_order_edition import reject_order_edition
from app.order.serivices.admin.confirm_delivery_edition import confirm_delivery_to_courier
from app.order.serivices.user.querys.get_orders import get_user_orders
from app.order.schemas.outputs import OrderResponse


router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/user/buy",response_model= OrderResponse)
async def buy(edition_ids: list[int] ,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await create_order(uow=uow,token_data=token_data,edition_ids=edition_ids)

@router.patch("/user/cancel",response_model= OrderResponse)
async def Cancel_order(order_id:int ,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await cancel_order(uow=uow,token_data=token_data,order_id=order_id)

@router.get("/user/")
async def Get_order(uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await get_user_orders(uow=uow,token_data=token_data)

@router.get("/author/")
async def get_ordereditions(uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await get_order_edition(uow=uow,token_data=token_data)

@router.patch("/author/accept")
async def Accept_order_edition(order_edition_id: int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await accept_order_edition(uow=uow,token_data=token_data,order_edition_id=order_edition_id)

@router.patch("/author/reject")
async def reject_orderedition(order_edition_id: int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await reject_order_edition(uow=uow,token_data=token_data,order_edition_id=order_edition_id)

@router.patch("/admin")
async def confirm_delivery(order_edition_id: int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await confirm_delivery_to_courier(uow=uow,token_data=token_data,order_edition_id=order_edition_id)