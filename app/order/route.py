from fastapi import APIRouter, Depends, Request
from app.security import get_current_user
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
from dependency_injector.wiring import inject, Provide
from app.dependency_injection.container import Container


router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/user/buy",response_model= OrderResponse)
@limiter.limit("5/minute")
@inject
async def buy(request: Request, edition_ids: list[int] ,handeler = Depends(get_idempotency_handler), uow = Depends((Provide[Container.uow])),token_data = Depends(get_current_user),idempotency_key: str = Depends(get_idempotency_key)):
    # return await create_order(uow=uow,token_data=token_data,edition_ids=edition_ids)
    return await handeler(key=idempotency_key,usecase=create_order,uow=uow,token_data=token_data,edition_ids=edition_ids)



@router.patch("/user/cancel",response_model= OrderResponse)
@limiter.limit("5/minute")
@inject
async def Cancel_order(request: Request, order_id:int ,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await cancel_order(uow=uow,token_data=token_data,order_id=order_id)

@router.get("/user/")
@limiter.limit("5/minute")
@inject
async def Get_order(request: Request, uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await get_user_orders(uow=uow,token_data=token_data)

@router.get("/author/")
@limiter.limit("5/minute")
@inject
async def get_ordereditions(request: Request, uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await get_order_edition(uow=uow,token_data=token_data)

@router.patch("/author/accept")
@limiter.limit("5/minute")
@inject
async def Accept_order_edition(request: Request, order_edition_id: int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await accept_order_edition(uow=uow,token_data=token_data,order_edition_id=order_edition_id)

@router.patch("/author/reject")
@limiter.limit("5/minute")
@inject
async def reject_orderedition(request: Request, order_edition_id: int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await reject_order_edition(uow=uow,token_data=token_data,order_edition_id=order_edition_id)

@router.patch("/admin")
@limiter.limit("5/minute")
@inject
async def confirm_delivery(request: Request, order_edition_id: int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await confirm_delivery_to_courier(uow=uow,token_data=token_data,order_edition_id=order_edition_id)