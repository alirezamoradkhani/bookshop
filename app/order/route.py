from fastapi import APIRouter, Depends, Request
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.order.serivices.user.command.create_oreder import create_order
from app.order.serivices.user.command.cancel_order import cancel_order
from app.order.serivices.author.querys.get_orderedition import get_order_edition
from app.order.serivices.author.command.accept_order_edition import accept_order_edition
from app.order.serivices.author.command.reject_order_edition import reject_order_edition
from app.order.serivices.admin.command.confirm_delivery_edition import confirm_delivery_to_courier
from app.order.serivices.user.querys.get_orders import get_user_orders
from app.order.schemas.outputs import OrderResponse
from app.Idempotency.dependency import get_idempotency_handler
from app.Idempotency.get_idempotency_key import get_idempotency_key
from app.ratelimiter.limiter import limiter

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/user/buy",response_model= OrderResponse)
@limiter.limit("5/minute")
async def buy(request: Request, edition_ids: list[int] ,handeler = Depends(get_idempotency_handler), uow = Depends(get_uow),token_data = Depends(get_current_user),idempotency_key: str = Depends(get_idempotency_key)):
    # return await create_order(uow=uow,token_data=token_data,edition_ids=edition_ids)
    return await handeler(key=idempotency_key,usecase=create_order,uow=uow,token_data=token_data,edition_ids=edition_ids)



@router.patch("/user/cancel",response_model= OrderResponse)
@limiter.limit("5/minute")
async def Cancel_order(request: Request, order_id:int ,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await cancel_order(uow=uow,token_data=token_data,order_id=order_id)

@router.get("/user/")
@limiter.limit("5/minute")
async def Get_order(request: Request, uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await get_user_orders(uow=uow,token_data=token_data)

@router.get("/author/")
@limiter.limit("5/minute")
async def get_ordereditions(request: Request, uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await get_order_edition(uow=uow,token_data=token_data)

@router.patch("/author/accept")
@limiter.limit("5/minute")
async def Accept_order_edition(request: Request, order_edition_id: int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await accept_order_edition(uow=uow,token_data=token_data,order_edition_id=order_edition_id)

@router.patch("/author/reject")
@limiter.limit("5/minute")
async def reject_orderedition(request: Request, order_edition_id: int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await reject_order_edition(uow=uow,token_data=token_data,order_edition_id=order_edition_id)

@router.patch("/admin")
@limiter.limit("5/minute")
async def confirm_delivery(request: Request, order_edition_id: int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await confirm_delivery_to_courier(uow=uow,token_data=token_data,order_edition_id=order_edition_id)